#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import errno
import re
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import logging
import traceback
import codecs
import shutil
import json
import argparse

# --- Try importing required libraries, provide clear errors if missing ---
try:
    import yaml
except ImportError:
    print >> sys.stderr, "ERROR: PyYAML library not found. Please install it: pip install PyYAML"
    sys.exit(1)

try:
    from jinja2 import Environment, StrictUndefined, exceptions as jinja_exc
except ImportError:
    print >> sys.stderr, "ERROR: Jinja2 library not found. Please install it: pip install Jinja2"
    sys.exit(1)

try:
    # Requires installation: pip install beautifulsoup4 lxml
    from bs4 import BeautifulSoup
except ImportError:
    # Only critical if HTML processing is actually used
    BeautifulSoup = None # Define as None if not found
    logging.warning("BeautifulSoup4 library not found (pip install beautifulsoup4 lxml). HTML processing will fail if attempted.")


# --- Python 2 compatibility ---
try:
    text_type = unicode # In Python 2, unicode is the text type
except NameError:
    text_type = str     # In Python 3, str is the text type

# ---------------------------------------------------------------------------
# 基础工具 & 异常
# ---------------------------------------------------------------------------
class SyncError(RuntimeError):
    """脚本执行中可预期的业务错误（非编程错误）"""
    pass # No need to repeat the docstring if it's the same

def _mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        # In Python 2, EEXIST might not be defined in os, use errno
        if exc.errno != errno.EEXIST or not os.path.isdir(path):
            raise

def _sanitize(s):
    """去掉可能的非法文件名字符，仅保留 [A-Za-z0-9_.-]"""
    if isinstance(s, str): # Check against Python 2's byte string type 'str'
        try:
            s = s.decode('utf-8', 'ignore')
        except UnicodeDecodeError: # Handle potential decoding errors more gracefully
             # Fallback or alternative decoding if utf-8 fails
             try:
                 s = s.decode(sys.getfilesystemencoding(), 'ignore')
             except Exception:
                 # If all else fails, represent bytes safely
                 s = repr(s)

    elif not isinstance(s, text_type): # Ensure we only process text types further
        s = text_type(s) # Convert other types to text

    # Use unicode pattern with unicode replacement
    return re.sub(u'[^\w.-]+', u'', s, flags=re.UNICODE)


def _tostring_pretty(elem):
    # ET.tostring returns bytes (str in Python 2)
    raw = ET.tostring(elem, 'utf-8')
    try:
        # minidom expects bytes
        reparsed = minidom.parseString(raw)
        # toprettyxml returns bytes if encoding is specified
        pretty = reparsed.toprettyxml(indent='  ', encoding='utf-8') # Use 2 spaces indent
    except Exception as e:
        logging.warning("XML pretty printing failed: %s. Falling back to raw output.", e)
        # Ensure raw ends with a newline (as bytes)
        return raw if raw.endswith(b'\n') else raw + b'\n'

    # Process lines as bytes
    lines = [l for l in pretty.splitlines() if l.strip()]
    return b'\n'.join(lines) + b'\n'

# ---------------------------------------------------------------------------
# 主业务类
# ---------------------------------------------------------------------------
class ManifestRepoSync(object):
    """封装整个流程"""

    def __init__(self, args):
        self.args = args
        # Ensure product name is decoded correctly and sanitized
        self.product = _sanitize(self._decode(args.product))
        if not self.product:
             raise SyncError("Resulting product name after sanitization is empty.")

        self.workdir = os.path.abspath(self.product)
        self.include_dir = os.path.join(self.workdir, u'include') # Use unicode literal
        self.env = Environment(undefined=StrictUndefined)
        self.config = {}
        self.html_path = None # Initialize before _html_present
        self.html_manifest_path = None
        self.repo_report = []            # [{xml, status, error}]

        # Configure logging (basic setup, can be enhanced)
        log_level = logging.DEBUG if os.environ.get('DEBUG') else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s [%(levelname)-7s] %(message)s', # Adjusted format
            datefmt='%Y-%m-%d %H:%M:%S' # Added date format
        )
        logging.info("Initialized ManifestRepoSync for product: %s", self.product)
        logging.info("Working directory: %s", self.workdir)


    # ------------------------- 公共入口 ------------------------- #
    def run(self):
        try:
            self._load_and_merge_config()
            if self._html_present():
                self._build_manifest_from_html()
            self._process_input_xmls()
            if self.args.create_repos:
                self._create_repos()
            self._write_summary()
            logging.info('===== ALL TASKS FINISHED SUCCESSFULLY =====')
        except SyncError as e:
            logging.error('ABORT: %s', e)
            sys.exit(2)
        except Exception as e:
            logging.critical('UNEXPECTED ERROR: %s', e)
            logging.debug(traceback.format_exc()) # Log traceback on DEBUG level
            sys.exit(1)

    # ----------------------- 阶段 1：配置 ----------------------- #
    def _load_and_merge_config(self):
        logging.info("Loading and merging configuration...")
        def _safe_load(path):
            logging.debug("Attempting to load config: %s", path)
            # Use absolute path for base config as well
            abs_path = os.path.abspath(path)
            if not os.path.exists(abs_path):
                logging.warning("Config file not found: %s", abs_path)
                return {}
            try:
                # Use codecs.open for reliable UTF-8 reading in Python 2
                with codecs.open(abs_path, 'r', 'utf-8') as fp:
                    # Handle empty file gracefully
                    content = fp.read()
                    if not content.strip():
                        logging.warning("Config file is empty: %s", abs_path)
                        return {}
                    # Reset pointer and load yaml
                    fp.seek(0)
                    data = yaml.safe_load(fp)
                    logging.debug("Successfully loaded YAML from %s", abs_path)
                    # Ensure it returns a dict even if YAML content is null/empty
                    return data if isinstance(data, dict) else {}
            except yaml.YAMLError as e:
                 logging.error("Error parsing YAML file %s: %s", abs_path, e)
                 raise SyncError("Invalid YAML format in %s" % abs_path)
            except Exception as e:
                 logging.error("Error reading config file %s: %s", abs_path, e)
                 raise SyncError("Cannot read config file %s" % abs_path)


        # Load base config (relative to script or absolute)
        base_cfg = _safe_load(self.args.base_config)
        # Load overlay config (relative to workdir)
        overlay_cfg = _safe_load(os.path.join(self.workdir, u'overlay.yaml')) # Use unicode

        # Deep merge function
        def _merge(a, b):
            if isinstance(a, dict) and isinstance(b, dict):
                # Start with a copy of a
                res = a.copy()
                # Iterate over b's items
                for k, v_b in b.items():
                    # If key exists in a and both values are dicts, recurse
                    if k in res and isinstance(res[k], dict) and isinstance(v_b, dict):
                        res[k] = _merge(res[k], v_b)
                    # Otherwise, b's value overrides a's value (including None)
                    # Note: If v_b is None, it *will* overwrite a non-None value in a.
                    # If you want None in b to not overwrite, change the following line.
                    else:
                        res[k] = v_b # b takes precedence
                return res
            # If not merging dicts, b takes precedence if it's not None, otherwise a
            return b if b is not None else a

        logging.debug("Merging base and overlay configurations...")
        self.config = _merge(base_cfg, overlay_cfg)

        # Ensure baseline section exists and add product name
        self.config.setdefault('baseline', {})['product'] = self.product
        logging.info("Configuration loaded and merged successfully.")
        # logging.debug("Final merged config: %s", json.dumps(self.config, indent=2))


    # --------------------- 阶段 2：HTML -> manifest -------------- #
    def _html_present(self):
        default_html = os.path.join(self.workdir, u'about.html') # Use unicode
        self.html_path = self.args.html or default_html
        logging.debug("Checking for HTML file at: %s", self.html_path)
        is_present = os.path.isfile(self.html_path)
        if is_present:
             logging.info("HTML file found: %s", self.html_path)
        else:
             logging.info("HTML file not found at expected location: %s", self.html_path)
        return is_present

    def _build_manifest_from_html(self):
        if BeautifulSoup is None:
             raise SyncError("Cannot process HTML: BeautifulSoup4 library is not installed (pip install beautifulsoup4 lxml).")

        logging.info('Processing HTML: %s', self.html_path)
        try:
            # Use codecs.open for reliable reading, ignore errors cautiously
            with codecs.open(self.html_path, 'r', 'utf-8', errors='ignore') as fp:
                html_content = fp.read()
            # Specify lxml parser
            soup = BeautifulSoup(html_content, 'lxml')
        except Exception as e:
            raise SyncError("Failed to read or parse HTML file %s: %s" % (self.html_path, e))

        # Product family extraction (Robustness improved)
        pf = u'manifest' # Default product family name
        pf_cell = soup.find('table', class_='build')
        if pf_cell:
            logging.debug("Found build table.")
            # Find the header cell robustly
            hit = pf_cell.find(lambda tag: tag.name in ('th', 'td') and u'Software Product Family' in tag.get_text(strip=True))
            if hit:
                logging.debug("Found 'Software Product Family' header.")
                # Find the next actual data cell (td or th)
                val = hit.find_next_sibling(lambda tag: tag.name in ('td', 'th'))
                if val:
                    pf_text = val.get_text(strip=True)
                    if pf_text:
                        pf = _sanitize(pf_text)
                        logging.info('Product family extracted from HTML: %s', pf)
                    else:
                        logging.warning("Product family cell found but is empty.")
                else:
                    logging.warning("Found product family header but no value cell next to it.")
            else:
                logging.warning("Could not find 'Software Product Family' in the build table.")
        else:
            logging.warning('Could not find <table class="build"> in HTML. Using default product family "%s".', pf)


        # Component table extraction (Robustness improved)
        comp_table = soup.find('table', class_='component')
        if not comp_table:
            # Don't raise error, maybe HTML processing is optional or fallback exists
            logging.warning('Cannot find <table class="component"> in HTML. No projects extracted from HTML.')
            return # Exit gracefully if table not found

        projects = []
        # Iterate over table rows, skipping header (assume first row is header)
        for row in comp_table.find_all('tr')[1:]:
            cols = row.find_all('td')
            # Expect at least 4 columns for name and path (indices 1 and 3)
            if len(cols) >= 4:
                name = cols[1].get_text(strip=True)
                path = cols[3].get_text(strip=True)
                # Only add if both name and path are non-empty
                if name and path:
                    projects.append({'name': name, 'path': path})
                else:
                    logging.debug("Skipping row in component table: name or path is empty.")
            else:
                logging.debug("Skipping row in component table: less than 4 columns.")

        if not projects:
             logging.warning("Found component table but extracted 0 valid projects from HTML.")
             self.html_manifest_path = None # 确保路径为 None
             return # 如果没有项目，也直接返回

        logging.info(u"已从 HTML 中成功提取 %d 个项目信息如下:", len(projects)) # 使用 unicode
        # 循环打印每个项目的信息到日志
        for i, p in enumerate(projects):
            # 使用 logging.info 输出到终端日志
            logging.info(u"  项目 [%d/%d] - 名称: %s, 路径: %s",
                         i + 1, len(projects), p['name'], p['path']) # 确保日志信息是 unicode

        # --- 修改点：移除文件路径计算和文件写入 ---
        # # Define output path using the extracted product family
        # out_name = u'%s_from_html.xml' % pf # Make filename distinct
        # self.html_manifest_path = os.path.join(self.workdir, out_name) # Store the path
        self.html_manifest_path = None # <<< 关键：将路径设为 None，表示没有生成文件
        # _mkdir_p(self.workdir) # Ensure workdir exists # 如果不写入文件则不需要创建目录

        # # Write the generated XML
        # # self._write_xml(xml_root, self.html_manifest_path) # <<< 关键：移除或注释掉文件写入调用

        # 修改日志消息，说明信息已记录但未生成文件
        logging.info(u'HTML 项目信息已记录到日志 (注意：未生成对应的 XML 文件)。') # 使用 unicode


    # ------------------- 阶段 3：XML -> include/*.xml -------------- #
    def _process_input_xmls(self):
        logging.info("Processing input XML manifest operations...")
        _mkdir_p(self.include_dir)
        ops = self.config.get('operations', [])
        if not ops:
            logging.info('No "operations" defined in config; skipping XML processing.')
            return

        baseline = self.config.get('baseline', {}).get('product', u'')
        logging.debug("Using baseline prefix: %s", baseline if baseline else "None")

        # Initialize special manifests
        special_remove = ET.Element('manifest')
        special_full = ET.Element('manifest')
        processed_files = 0

        for i, op in enumerate(ops):
            infile = op.get('file')
            if not infile:
                logging.warning("Operation #%d skipped: missing 'file' attribute.", i + 1)
                continue

            # Use unicode for paths
            src = os.path.join(self.workdir, self._decode(infile))
            if not os.path.isfile(src):
                logging.warning('Operation #%d skipped: Input XML not found: %s', i + 1, src)
                continue

            logging.info("Processing operation #%d: %s", i + 1, infile)
            try:
                root = ET.parse(src).getroot()
            except ET.ParseError as e:
                 logging.error("Failed to parse XML file %s: %s", src, e)
                 self.repo_report.append({'xml': infile, 'status': 'FAIL', 'error': 'XML Parse Error: %s' % e}) # Add error report
                 continue # Skip this file
            except Exception as e:
                 logging.error("Failed to read XML file %s: %s", src, e)
                 self.repo_report.append({'xml': infile, 'status': 'FAIL', 'error': 'XML Read Error: %s' % e})
                 continue


            # --- Calculate name/path prefixes using Jinja ---
            ctx = {'common': self.config.get('common', {}),
                   'filename': os.path.splitext(infile)[0]} # Context for Jinja

            # Name Prefix
            name_prefix_template = op.get('name_prefix', None) # Check if explicitly set
            if name_prefix_template is None: # If not set in op, use common default
                 name_prefix_template = self.config.get('common', {}).get('name_prefix_template', u'')
            rendered_name_prefix = self._render(name_prefix_template, ctx)
            name_prefix = self._join(baseline, rendered_name_prefix) # Join with baseline

            # --- *** FIX: Path Prefix Logic *** ---
            if 'path_prefix' in op:
                # Path prefix EXPLICITLY defined in the operation (even if "").
                path_prefix_template = op['path_prefix']
                logging.debug("Using explicit path_prefix from operation: '%s'", path_prefix_template)
            else:
                # Path prefix NOT defined in op, fall back to common default.
                path_prefix_template = self.config.get('common', {}).get('path_prefix_template', u'')
                logging.debug("Using default path_prefix template: '%s'", path_prefix_template)
            # Render the chosen template (could be empty string)
            # Pass only 'common' context, as specified in original logic
            path_prefix = self._render(path_prefix_template, {'common': ctx['common']})
            # path_prefix might be u'' here if explicitly set or rendered that way

            logging.debug("Calculated name_prefix: %s", name_prefix)
            logging.debug("Calculated path_prefix: %s", path_prefix)

            all_root = ET.Element('manifest')
            project_count = 0
            special_project_count = 0

            for proj in root.findall('.//project'): # Find all 'project' elements anywhere
                project_count += 1
                name_attr = proj.get('name')
                if not name_attr:
                     logging.warning("Skipping project in %s: missing 'name' attribute.", infile)
                     continue

                # Ensure name is unicode and clean .git suffix
                n = self._decode(name_attr)
                if n.endswith(u'.git'):
                    n = n[:-4]

                # Path defaults to name if not specified
                p = self._decode(proj.get('path', n))

                # Apply prefixes using the corrected _join method
                full_n = self._join(name_prefix, n)
                # Apply the potentially empty path_prefix
                full_p = self._join(path_prefix, p)

                logging.debug("  Project: name='%s', path='%s' -> full_name='%s', full_path='%s'", n, p, full_n, full_p)

                # Add to the *_all_projects.xml manifest for this file
                ET.SubElement(all_root, 'project', name=full_n, path=full_p)

                # --- Handle special projects (linkfile/copyfile) ---
                linkfiles = proj.findall('linkfile')
                copyfiles = proj.findall('copyfile')

                if linkfiles or copyfiles:
                    special_project_count += 1
                    logging.debug("    Found special project with linkfile/copyfile.")
                    # 1. Add to the global remove-project list
                    ET.SubElement(special_remove, 'remove-project', name=full_n)

                    # 2. Create the full project entry for the special manifest
                    sp = ET.Element('project', name=full_n, path=full_p)
                    for tag_name, elements in [(u'linkfile', linkfiles), (u'copyfile', copyfiles)]:
                        for child in elements:
                            src_attr = child.get('src')
                            dest_attr = child.get('dest')
                            if src_attr and dest_attr:
                                # Apply path_prefix ONLY to the destination
                                full_dest = self._join(path_prefix, self._decode(dest_attr))
                                ET.SubElement(sp, tag_name,
                                              src=self._decode(src_attr), # Keep src relative? Check manifest format spec
                                              dest=full_dest)
                            else:
                                logging.warning("    Skipping %s in special project %s: missing src or dest.", tag_name, full_n)
                    # Add the fully formed special project to the global special_full manifest
                    special_full.append(sp)


            # Write the *_all_projects.xml for this individual input file
            if project_count > 0:
                 # Use unicode filename, replacing potential bad chars
                 safe_infile_base = _sanitize(os.path.splitext(infile)[0])
                 dst = os.path.join(
                     self.include_dir,
                     u'%s_all_projects.xml' % safe_infile_base
                 )
                 self._write_xml(all_root, dst)
                 processed_files += 1
            else:
                 logging.warning("No projects found or processed in %s.", infile)

            logging.info("Finished processing %s (%d projects, %d special).", infile, project_count, special_project_count)


        # --- Final write for global special manifests ---
        if len(special_remove):
            self._write_xml(special_remove,
                            os.path.join(self.include_dir, u'special_remove_projects.xml')) # More descriptive name
        if len(special_full):
            self._write_xml(special_full,
                            os.path.join(self.include_dir, u'special_full_projects.xml')) # More descriptive name

        logging.info("Finished processing all %d input XML files.", processed_files)


    # ----------------- 阶段 4：创建裸仓库 ------------------------ #
    def _create_repos(self):
        logging.info("Starting repository creation process...")
        # Render templates for demo repo and output directory
        demo_tpl = (self.args.demo_path or
                    self.config.get('common', {}).get('demo', u''))
        out_tpl = (self.args.output_dir or
                   self.config.get('common', {}).get('output', u''))

        # Context includes baseline and common sections
        ctx = {'baseline': self.config.get('baseline', {}),
               'common': self.config.get('common', {})}

        demo_repo = self._render(demo_tpl, ctx)
        out_dir = self._render(out_tpl, ctx)

        if not demo_repo:
            raise SyncError('Demo repository path (common.demo or --demo-path) is not defined or evaluates to empty.')
        if not out_dir:
            raise SyncError('Output directory path (common.output or --output-dir) is not defined or evaluates to empty.')

        # Make paths absolute for robustness
        demo_repo = os.path.abspath(demo_repo)
        out_dir = os.path.abspath(out_dir)

        logging.info("Using demo repository: %s", demo_repo)
        logging.info("Output directory for new repos: %s", out_dir)

        # --- Collect manifests to process ---
        manifests_to_process = []
        # 1. Manifest generated from HTML (if any)
        if self.html_manifest_path and os.path.isfile(self.html_manifest_path):
            manifests_to_process.append(self.html_manifest_path)
            logging.debug("Added HTML-generated manifest to processing list: %s", self.html_manifest_path)

        # 2. Manifests declared in config 'projects' section
        for i, prj in enumerate(self.config.get('projects', [])):
            manifest_template = prj.get('manifest', u'')
            if manifest_template:
                # Render the manifest path template
                rendered_manifest_path = self._render(manifest_template, ctx)
                if rendered_manifest_path:
                    # Assume relative to workdir unless absolute
                    abs_manifest_path = os.path.join(self.workdir, rendered_manifest_path) if not os.path.isabs(rendered_manifest_path) else rendered_manifest_path
                    if os.path.isfile(abs_manifest_path):
                        manifests_to_process.append(abs_manifest_path)
                        logging.debug("Added manifest from config project #%d: %s", i+1, abs_manifest_path)
                    else:
                        logging.warning("Manifest specified in config project #%d not found: %s (tried %s)", i+1, manifest_template, abs_manifest_path)
                else:
                     logging.warning("Manifest template in config project #%d rendered to empty string.", i+1)
            else:
                 logging.debug("Config project #%d has no 'manifest' key.", i+1)

        if not manifests_to_process:
             logging.warning("No valid manifest files found to process for repository creation.")
             return # Nothing to do

        logging.info("Found %d manifest(s) to process for repo creation.", len(manifests_to_process))

        # --- Process each manifest ---
        for mfile_path in manifests_to_process:
            mfile_basename = os.path.basename(mfile_path)
            logging.info("Processing manifest for repo creation: %s", mfile_basename)
            status = u'OK'
            error = u''
            try:
                # Pass absolute paths
                self._create_repos_from_manifest(mfile_path, demo_repo, out_dir)
            except SyncError as e: # Catch specific expected errors
                 status = u'FAIL'
                 error = text_type(e)
                 logging.error('Repo creation failed for %s: %s', mfile_basename, e)
            except Exception as e: # Catch unexpected errors
                status = u'FAIL'
                error = u'Unexpected Error: %s' % text_type(e)
                logging.error('Unexpected error during repo creation for %s: %s', mfile_basename, e)
                logging.debug(traceback.format_exc()) # Log traceback for unexpected errors

            # Append report entry (use unicode)
            self.repo_report.append({'xml': mfile_basename,
                                     'status': status,
                                     'error': error})

        logging.info("Finished repository creation attempts.")


    def _create_repos_from_manifest(self, manifest_path, demo_repo, out_dir):
        # Input paths are already absolute and validated where possible
        if not os.path.exists(demo_repo):
            raise SyncError('Demo repo disappeared unexpectedly: %s' % demo_repo) # Should not happen if checked before

        # Ensure output directory exists (might have been created by another process)
        _mkdir_p(out_dir)

        logging.debug("Parsing manifest: %s", manifest_path)
        try:
            tree = ET.parse(manifest_path)
            root = tree.getroot()
        except ET.ParseError as e:
             raise SyncError("Cannot parse manifest XML %s: %s" % (os.path.basename(manifest_path), e))
        except Exception as e:
             raise SyncError("Cannot read manifest XML %s: %s" % (os.path.basename(manifest_path), e))


        projects_in_manifest = []
        # Use XPath to find all project elements, regardless of hierarchy
        for proj in root.findall('.//project'):
            name_attr = proj.get('name')
            if not name_attr:
                 logging.warning("Skipping project in %s: missing 'name' attribute", os.path.basename(manifest_path))
                 continue

            # Get path, defaulting to name
            path_attr = proj.get('path', name_attr)

            # Decode and store
            projects_in_manifest.append({
                'name': self._decode(name_attr),
                'path': self._decode(path_attr) # path is informational here
            })

        if not projects_in_manifest:
             logging.warning("Manifest %s contains no valid <project> elements.", os.path.basename(manifest_path))
             return # Nothing to create for this manifest

        logging.info("Manifest %s: Found %d projects to create/update.",
                     os.path.basename(manifest_path), len(projects_in_manifest))

        total_projects = len(projects_in_manifest) # 获取总数


        created_count = 0
        skipped_count = 0
        error_count = 0
        # --- 优化点：定义日志间隔 ---
        LOG_INTERVAL = 20 # 每处理 20 个仓库报告一次进度，您可以调整这个数值

        for i, proj_info in enumerate(projects_in_manifest):
            proj_name = proj_info['name']
            # Construct destination path for the bare repo
            # Ensure repo name doesn't contain slashes if used directly in path
            safe_repo_name = proj_name.replace('/', '_') # Example: replace slash with underscore
            repo_dest = os.path.join(out_dir, u'%s.git' % safe_repo_name) # Use unicode

            logging.debug("Processing project %d/%d: %s -> %s", i+1, len(projects_in_manifest), proj_name, repo_dest)

            try:
                # Check if destination exists (using os.path.exists handles dir/file)
                if os.path.exists(repo_dest):
                    # Optional: Decide whether to overwrite or skip
                    # Current logic overwrites by removing first
                    logging.debug("Destination exists, removing: %s", repo_dest)
                    shutil.rmtree(repo_dest) # shutil.rmtree handles non-empty dirs

                # Ensure parent directory of destination exists
                _mkdir_p(os.path.dirname(repo_dest))

                # Copy the demo repository GENTLY. Avoid full copy if only .git is needed.
                # For a bare repo, copying just the essential .git parts might be faster,
                # but copying the whole demo is simpler and matches original logic.
                # Use shutil.copytree
                #logging.debug("Copying demo repo to %s", repo_dest)
                shutil.copytree(demo_repo, repo_dest)
                created_count += 1
                #logging.info("Created repo [%d/%d] %s", i+1, len(projects_in_manifest), repo_dest)
                # --- 优化点：使用间隔日志替换原来的 INFO 日志 ---
                # 如果是最后一个，或者达到间隔数，则打印进度日志
                if (i + 1) % LOG_INTERVAL == 0 or (i + 1) == total_projects:
                    logging.info(u"...Created %d/%d repositories (from Manifest: %s)...",
                                 i + 1, total_projects, os.path.basename(manifest_path)) # 使用 unicode

            except OSError as e:
                 # Handle specific OS errors like permission denied
                 logging.error("OS Error creating repo %s (from %s): %s", repo_dest, proj_name, e)
                 error_count += 1
                 # Add error to main report as well? Decide on granularity.
                 # self.repo_report.append(...) # Can add more detail here if needed
                 continue # Continue with the next project
            except Exception as e:
                 # Handle other unexpected errors during copy/remove
                 logging.error("Unexpected Error creating repo %s (from %s): %s", repo_dest, proj_name, e)
                 logging.debug(traceback.format_exc())
                 error_count += 1
                 continue # Continue with the next project

            # Optional: Log progress periodically
            # if (i + 1) % 50 == 0:
            #     logging.info("...Processed %d/%d projects for this manifest...", i + 1, len(projects_in_manifest))


        logging.info("Finished processing manifest %s: %d created, %d skipped (if implemented), %d errors.",
                     os.path.basename(manifest_path), created_count, skipped_count, error_count)
        if error_count > 0:
             # Raise an error specific to this manifest if any project failed within it
             raise SyncError("Encountered %d error(s) while creating repositories for manifest %s. See logs for details."
                             % (error_count, os.path.basename(manifest_path)))


    # --------------------- 阶段 5：结果总结 ---------------------- #
    def _write_summary(self):
        # Only write summary if repo creation was attempted
        if not self.args.create_repos:
            logging.debug("Skipping summary writing as --create-repos was not specified.")
            return
        if not self.repo_report:
            logging.info("No repository creation tasks were performed or reported.")
            return

        # Use unicode path
        report_path = os.path.join(self.workdir, u'repo_summary.json')
        logging.info("Writing repository creation summary to: %s", report_path)
        try:
            # Use codecs.open for writing JSON with UTF-8 in Python 2
            with codecs.open(report_path, 'w', encoding='utf-8') as fp:
                # ensure_ascii=False is crucial for non-ASCII chars in JSON with utf-8 file
                json.dump(self.repo_report, fp, indent=2, sort_keys=True, ensure_ascii=False)
        except IOError as e:
             logging.error("Failed to write summary file %s: %s", report_path, e)
             # Don't raise, just log the error
             return
        except Exception as e:
             logging.error("Unexpected error writing JSON summary %s: %s", report_path, e)
             return


        # Log summary status to console
        fail_count = sum(1 for r in self.repo_report if r['status'] == u'FAIL')
        ok_count = sum(1 for r in self.repo_report if r['status'] == u'OK') # Assuming OK is the success status

        if fail_count > 0:
            logging.warning('===== Repository Creation Summary =====')
            logging.warning('TOTAL Manifests Processed: %d', len(self.repo_report))
            logging.warning('SUCCESSFUL Manifests: %d', ok_count)
            logging.warning('FAILED Manifests: %d', fail_count)
            logging.warning('See %s for details on failures.', report_path)
            # Optionally, list failed manifests here
            for report in self.repo_report:
                if report['status'] == u'FAIL':
                    logging.warning("  - FAILED: %s (Error: %s)", report['xml'], report['error'][:100] + ('...' if len(report['error']) > 100 else ''))

        else:
            logging.info('===== Repository Creation Summary =====')
            logging.info('All %d manifests processed successfully for repository creation.', len(self.repo_report))
            logging.info('Summary details available at %s', report_path)


    # ------------------------- 工具方法 ------------------------- #
    @staticmethod
    def _join(prefix, name):
        """Joins prefix and name like a URL path, handling slashes."""
        # Ensure both are unicode
        prefix = text_type(prefix or u'')
        name = text_type(name or u'')

        if not prefix:
            return name.strip(u'/') # Return name cleaned
        if not name:
            return prefix.rstrip(u'/') # Return prefix cleaned

        # Join, ensuring only one slash between non-empty parts
        return u'%s/%s' % (prefix.rstrip(u'/'), name.lstrip(u'/'))


    @staticmethod
    def _write_xml(root, path):
        _mkdir_p(os.path.dirname(path))
        try:
            xml_bytes = _tostring_pretty(root)
            with open(path, 'wb') as fp: # Open in binary write mode
                fp.write(xml_bytes)
            logging.info('Wrote XML: %s (%d bytes)', path, len(xml_bytes))
        except IOError as e:
             logging.error("Failed to write XML file %s: %s", path, e)
             # Optionally raise or handle
        except Exception as e:
             logging.error("Unexpected error writing XML %s: %s", path, e)


    def _render(self, template_or_val, context):
        # Ensure input is unicode for Jinja
        template_str = self._decode(template_or_val or u'')

        # Only process if it looks like a Jinja template
        if u'{{' in template_str or u'{%' in template_str or u'{#' in template_str:
            try:
                template = self.env.from_string(template_str)
                rendered = template.render(context)
                logging.debug("Rendered template '%s' -> '%s'", template_str, rendered)
                return rendered # Jinja returns unicode
            except jinja_exc.UndefinedError as e:
                 # Provide more context for undefined variable errors
                 logging.error("Jinja rendering error: Undefined variable. %s", e)
                 logging.error("Template snippet: '%s'", template_str)
                 logging.error("Context keys available: %s", context.keys())
                 raise SyncError('Jinja error: %s. Check template and context.' % e)
            except jinja_exc.TemplateError as e:
                 logging.error("Jinja rendering error: %s", e)
                 logging.error("Template snippet: '%s'", template_str)
                 raise SyncError('Jinja error: %s' % e)
            except Exception as e: # Catch other potential errors during rendering
                 logging.error("Unexpected error during Jinja rendering: %s", e)
                 logging.error("Template snippet: '%s'", template_str)
                 raise SyncError('Unexpected Jinja error: %s' % e)
        else:
            # If not a template, just return the value as unicode
            logging.debug("Value '%s' is not a Jinja template, using as is.", template_str)
            return template_str


    @staticmethod
    def _decode(b):
        """Decodes bytes to unicode using common encodings."""
        if isinstance(b, text_type): # Already unicode
            return b
        if isinstance(b, str): # Bytes in Python 2
            # Try common encodings
            for enc in ('utf-8', sys.getfilesystemencoding(), 'latin-1'):
                try:
                    return b.decode(enc)
                except UnicodeDecodeError:
                    continue # Try next encoding
                except Exception as e:
                     logging.warning("Decoding error with '%s' for bytes: %s", enc, e)
                     continue # Try next encoding
            # If all decodings fail, return a representation
            logging.warning("Could not decode bytes using common encodings, returning repr.")
            return repr(b)
        # If not bytes or unicode, try converting to text_type
        try:
            return text_type(b)
        except Exception as e:
             logging.error("Cannot convert non-string type %s to text: %s", type(b), e)
             return u'' # Return empty unicode string

# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------
def _parse_cli():
    p = argparse.ArgumentParser(
        description='Manifest processor & repository synchronizer (Python 2.7 Compatible)')

    p.add_argument('-p', '--product', required=True,
                   help='Target product name (will become working directory name)')

    p.add_argument('-repo', '--create-repos', action='store_true',
                   help='Create git repos in output dir after manifest processing')

    # Override paths from config
    p.add_argument('--demo-path', help='Override demo git repository path (used for creating new repos)')
    p.add_argument('--output-dir', help='Override base output directory for created git repos')

    # Configuration files
    p.add_argument('--base-config', default='base.yaml',
                   help='Base YAML configuration file path (default: base.yaml)')
    p.add_argument('--html', help='Optional input HTML file path (default: <product>/about.html)')

    # Add verbosity/debug flag?
    # p.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')

    return p.parse_args()

if __name__ == '__main__':
    # Basic check for Python version (optional)
    if sys.version_info[0] != 2 or sys.version_info[1] < 7:
         print >> sys.stderr, "ERROR: This script requires Python 2.7."
         sys.exit(1)

    # Ensure libraries are available early
    # (Imports are already checked at the top)

    args = _parse_cli()
    # Initialize and run the main process
    ManifestRepoSync(args).run()
