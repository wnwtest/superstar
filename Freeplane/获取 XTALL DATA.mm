<map version="freeplane 1.11.5">
<!--To view this file, download free mind mapping software Freeplane from https://www.freeplane.org -->
<node TEXT="获取 XTALL DATA" FOLDED="false" ID="ID_696401721" CREATED="1610381621824" MODIFIED="1712643829558" STYLE="oval">
<font SIZE="18"/>
<hook NAME="MapStyle">
    <properties edgeColorConfiguration="#808080ff,#ff0000ff,#0000ffff,#00ff00ff,#ff00ffff,#00ffffff,#7c0000ff,#00007cff,#007c00ff,#7c007cff,#007c7cff,#7c7c00ff" fit_to_viewport="false" associatedTemplateLocation="template:/standard-1.6.mm" show_note_icons="true"/>

<map_styles>
<stylenode LOCALIZED_TEXT="styles.root_node" STYLE="oval" UNIFORM_SHAPE="true" VGAP_QUANTITY="24 pt">
<font SIZE="24"/>
<stylenode LOCALIZED_TEXT="styles.predefined" POSITION="bottom_or_right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="default" ID="ID_271890427" ICON_SIZE="12 pt" COLOR="#000000" STYLE="fork">
<arrowlink SHAPE="CUBIC_CURVE" COLOR="#000000" WIDTH="2" TRANSPARENCY="200" DASH="" FONT_SIZE="9" FONT_FAMILY="SansSerif" DESTINATION="ID_271890427" STARTARROW="NONE" ENDARROW="DEFAULT"/>
<font NAME="SansSerif" SIZE="10" BOLD="false" ITALIC="false"/>
<richcontent TYPE="DETAILS" CONTENT-TYPE="plain/auto"/>
<richcontent TYPE="NOTE" CONTENT-TYPE="plain/auto"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.details"/>
<stylenode LOCALIZED_TEXT="defaultstyle.attributes">
<font SIZE="9"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.note" COLOR="#000000" BACKGROUND_COLOR="#ffffff" TEXT_ALIGN="LEFT"/>
<stylenode LOCALIZED_TEXT="defaultstyle.floating">
<edge STYLE="hide_edge"/>
<cloud COLOR="#f0f0f0" SHAPE="ROUND_RECT"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.selection" BACKGROUND_COLOR="#afd3f7" BORDER_COLOR_LIKE_EDGE="false" BORDER_COLOR="#afd3f7"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.user-defined" POSITION="bottom_or_right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="styles.topic" COLOR="#18898b" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subtopic" COLOR="#cc3300" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subsubtopic" COLOR="#669900">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.important" ID="ID_67550811">
<icon BUILTIN="yes"/>
<arrowlink COLOR="#003399" TRANSPARENCY="255" DESTINATION="ID_67550811"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.flower" COLOR="#ffffff" BACKGROUND_COLOR="#255aba" STYLE="oval" TEXT_ALIGN="CENTER" BORDER_WIDTH_LIKE_EDGE="false" BORDER_WIDTH="22 pt" BORDER_COLOR_LIKE_EDGE="false" BORDER_COLOR="#f9d71c" BORDER_DASH_LIKE_EDGE="false" BORDER_DASH="CLOSE_DOTS" MAX_WIDTH="6 cm" MIN_WIDTH="3 cm"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.AutomaticLayout" POSITION="bottom_or_right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="AutomaticLayout.level.root" COLOR="#000000" STYLE="oval" SHAPE_HORIZONTAL_MARGIN="10 pt" SHAPE_VERTICAL_MARGIN="10 pt">
<font SIZE="18"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,1" COLOR="#0033ff">
<font SIZE="16"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,2" COLOR="#00b439">
<font SIZE="14"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,3" COLOR="#990000">
<font SIZE="12"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,4" COLOR="#111111">
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,5"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,6"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,7"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,8"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,9"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,10"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,11"/>
</stylenode>
</stylenode>
</map_styles>
</hook>
<hook NAME="AutomaticEdgeColor" COUNTER="9" RULE="ON_BRANCH_CREATION"/>
<node TEXT="通过Vendor  tag 获取OTP数据" LOCALIZED_STYLE_REF="AutomaticLayout.level,1" POSITION="bottom_or_right" ID="ID_1623047762" CREATED="1712622142345" MODIFIED="1712622246929">
<edge COLOR="#ff0000"/>
<richcontent TYPE="NOTE">
<html>
  <head>
    
  </head>
  <body>
    <pre>   if (CDKResultSuccess == result)
    {
        result = ChiNodeUtils::GetVendorTagBase(&quot;org.codeaurora.qcamera3.sensor_meta_data&quot;,
                                                &quot;EEPROMInformation&quot;,
                                                &amp;g_ChiNodeInterface,
                                                &amp;vendorTagBase);
        if (CDKResultSuccess == result)
        {
            //LOG_ERROR(CamxLogGroupChi, &quot;get eeprom info vendor tag base&quot;);
            m_eepromInfoVendorTagBase = vendorTagBase.vendorTagBase;
        }
        else
        {
            LOG_ERROR(CamxLogGroupChi, &quot;Unable to get eeprom info vendor tag base&quot;);
        }
    }</pre>
  </body>
</html>
</richcontent>
<node TEXT="获取 Meta data" ID="ID_982765201" CREATED="1712622264091" MODIFIED="1712622433026"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <pre>    pData = ChiNodeUtils::GetMetaData(0,
                                              m_eepromInfoVendorTagBase | StaticMetadataSectionMask,
                                              ChiMetadataStatic,
                                              &amp;g_ChiNodeInterface,
                                              m_hChiSession);

    if (NULL != pData)
    {
                     

        eepromInfo                  = reinterpret_cast&lt;ChiEEPROMInformation*&gt;(pData);
        //LOG_ERROR(CamxLogGroupChi, &quot;EEPROMInfo  for InfoTag [%d] size %d &quot;, m_eepromInfoVendorTagBase,eepromInfo-&gt;rawOTPData.rawDataSize);             
        s5kgw3sp_otp_format( eepromInfo ); 
    }
    else
    {
            LOG_ERROR(CamxLogGroupChi, &quot;EEPROMInfo NULL for InfoTag [%d]&quot;, m_eepromInfoVendorTagBase);
            result = CDKResultEFailed;
    }
    </pre>
  </body>
</html>
</richcontent>
</node>
<node TEXT="对应的 vendor tag" ID="ID_1943464222" CREATED="1712622358538" MODIFIED="1712622425707"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <div>
      <div align="left" style="background-color: #ffffff; width: 378pt">
        <pre>&quot;org.codeaurora.qcamera3.sensor_meta_data&quot;</pre>
      </div>
    </div>
  </body>
</html>
</richcontent>
</node>
</node>
<node TEXT="CAMX新的 vendor tag" POSITION="top_or_left" ID="ID_1377866585" CREATED="1712643827393" MODIFIED="1712734690529" HGAP_QUANTITY="107 pt" VSHIFT_QUANTITY="-254.99999 pt">
<edge COLOR="#ff00ff"/>
<richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      camx/src/api/vendortag/camxvendortagdefines.h
    </p>
    <div style="color: #cccccc; background-color: #1f1f1f; font-family: Consolas, Courier New, monospace; font-weight: normal; font-size: 14px; line-height: 19px; white-space: pre">
      <div>
        <span style="color: #cccccc;">@@ -735,6 +735,12 @@ static CHIVENDORTAGSECTIONDATA g_HwVendorTagSections[] =</span>
      </div>
      <div>
        <span style="color: #cccccc;">&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;},</span>
      </div>
      <div>
        <span style="color: #cccccc;">&#xa0;</span>
      </div>
      <div>
        <span style="color: #cccccc;">&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;{</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&quot;org.quic.camera.CCStats&quot;, 0,</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;CAMX_ARRAY_SIZE(g_VendorTagSectionCCStats), g_VendorTagSectionCCStats,</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;CHITAGSECTIONVISIBILITY::ChiTagSectionVisibleToOEM</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;},</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+</span>
      </div>
    </div>
  </body>
</html>
</richcontent>
<node TEXT="PrepareRSStatsMetadata" ID="ID_1248887114" CREATED="1712728696708" MODIFIED="1712728779842"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <div style="color: #cccccc; background-color: #1f1f1f; font-family: Consolas, Courier New, monospace; font-weight: normal; font-size: 14px; line-height: 19px; white-space: pre">
      <div>
        <span style="color: #cccccc;">@@ -9405,6 +9437,45 @@ VOID IFENode::PrepareRSStatsMetadata(</span>
      </div>
      <div>
        <span style="color: #cccccc;">&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;pMetadata-&gt;statsConfig = pInputData-&gt;pCalculatedData-&gt;metadata.RSStats;</span>
      </div>
      <div>
        <span style="color: #cccccc;">&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;pMetadata-&gt;dualIFEMode = FALSE; </span>

        <div style="color: #cccccc; background-color: #1f1f1f; font-family: Consolas, Courier New, monospace; font-weight: normal; font-size: 14px; line-height: 19px; white-space: pre">
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;if (TRUE == IFEUtils::FindSensorStreamConfigIndex(StreamType::FLICKER_STATS, m_pSensorModeData, NULL))</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;{</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;UINT32 metaTag = 0;</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;result = VendorTagManager::QueryVendorTagLocation(</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&quot;org.quic.camera.CCStats&quot;, &quot;HasFlicker&quot;, &amp;metaTag);</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;if (CamxResultSuccess == result)</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;{</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;const UINT &#xa0;metadataTag[] = { metaTag | UsecaseMetadataSectionMask };</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;UINT8 &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;HasFlicker &#xa0;&#xa0;&#xa0;= 1;</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;const VOID* pDstData[1] &#xa0;&#xa0;= { &amp;HasFlicker };</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;UINT &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;pDataCount[1] = { 1 };</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;result = WriteDataList(metadataTag, pDstData, pDataCount, 1);</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;if (CamxResultSuccess != result)</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;{</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;CAMX_LOG_ERROR(CamxLogGroupISP, &quot;Node::%s Failed to publish CC Flicker stats existing&quot;,</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;NodeIdentifierString());</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;}</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;}</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;CAMX_LOG_VERBOSE(CamxLogGroupISP, &quot;CC Flicker stats existing&quot;);</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;}</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;else</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;{</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;CAMX_LOG_VERBOSE(CamxLogGroupISP, &quot;CC Flicker stats not existing&quot;);</span>
          </div>
          <div>
            <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;}</span>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>
</richcontent>
</node>
<node TEXT="设置vendor tag值" ID="ID_1175460369" CREATED="1712733286064" MODIFIED="1712733342659"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <div style="color: #cccccc; background-color: #1f1f1f; font-family: Consolas, Courier New, monospace; font-weight: normal; font-size: 14px; line-height: 19px; white-space: pre">
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;CAMX_INLINE VOID SetCCFlickerTag()</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;{</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;UINT32 metaTag = 0;</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;CamxResult result = VendorTagManager::QueryVendorTagLocation(</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&quot;org.quic.camera.CCStats&quot;, &quot;IsNullFlicker&quot;, &amp;metaTag);</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;if (CamxResultSuccess == result)</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;{</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;const UINT &#xa0;metadataTag[] = { metaTag };</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;UINT8 &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;IsNullFlicker = (CCHDRWorkingMode::Exposure1DOLMode == m_sensorCompanionData.workingMode) ?</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;1 : 0;</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;const VOID* pDstData[1] &#xa0;&#xa0;= { &amp;IsNullFlicker };</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;UINT &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;pDataCount[1] = { 1 };</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;CAMX_LOG_VERBOSE(CamxLogGroupSensor, &quot;IsNullFlicker %u&quot;, IsNullFlicker);</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;result = WriteDataList(metadataTag, pDstData, pDataCount, 1);</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;if (CamxResultSuccess != result)</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;{</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;CAMX_LOG_WARN(CamxLogGroupSensor, &quot;Node::%s Failed to publish CC Flicker stats status&quot;,</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;NodeIdentifierString());</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;}</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;}</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;};</span>
      </div>
    </div>
  </body>
</html>
</richcontent>
</node>
<node TEXT="获取vendor tag值" ID="ID_1690725509" CREATED="1712735137802" MODIFIED="1712735163501"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <div style="color: #cccccc; background-color: #1f1f1f; font-family: Consolas, Courier New, monospace; font-weight: normal; font-size: 14px; line-height: 19px; white-space: pre">
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;m_isCCFlickerExisting = FALSE;</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;if (TRUE == GetStaticSettings()-&gt;QCCompanionSensor)</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;{</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;UINT32 metaTag = 0;</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;CamxResult result = VendorTagManager::QueryVendorTagLocation(</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&quot;org.quic.camera.CCStats&quot;, &quot;HasFlicker&quot;, &amp;metaTag);</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;if (CamxResultSuccess == result)</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;{</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;UINT8 &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;HasFlicker &#xa0;= 0;</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;const UINT Props[] &#xa0;&#xa0;&#xa0;&#xa0;= {metaTag | UsecaseMetadataSectionMask};</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;VOID* &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;pData1[] &#xa0;&#xa0;&#xa0;= {NULL};</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;UINT64 &#xa0;&#xa0;&#xa0;&#xa0;offsets1[] &#xa0;= {0};</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;GetDataList(Props, pData1, offsets1, 1);</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;if (NULL != pData1[0])</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;{</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;HasFlicker = *reinterpret_cast&lt;UINT8*&gt;(pData1[0]);</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;}</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;m_isCCFlickerExisting = 1 == HasFlicker ? TRUE : FALSE;</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;CAMX_LOG_VERBOSE(CamxLogGroupStats, &quot;CC Flicker stats existing %u&quot;, m_isCCFlickerExisting);</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;}</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;}</span>
      </div>
    </div>
  </body>
</html>
</richcontent>
</node>
</node>
<node TEXT="CHI-CDK新的vendor tag" POSITION="bottom_or_right" ID="ID_673190615" CREATED="1712720628557" MODIFIED="1712727736608" HGAP_QUANTITY="-424.74999 pt" VSHIFT_QUANTITY="36.75 pt">
<edge COLOR="#00007c"/>
<richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      chi-cdk/api/common/chivendortagdefines.h
    </p>
    <div style="color: #cccccc; background-color: #1f1f1f; font-family: Consolas, Courier New, monospace; font-weight: normal; font-size: 14px; line-height: 19px; white-space: pre">
      <div>
        <span style="color: #cccccc;">@@ -766,6 +766,13 @@ static CHIVENDORTAGDATA g_VendorTagSectionMFNRConfigs[] =</span>
      </div>
      <div>
        <span style="color: #cccccc;">&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;{ &quot;MultiframeRequestTimestamp&quot;, &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;TYPE_INT64, &#xa0;&#xa0;1 &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;},</span>
      </div>
      <div>
        <span style="color: #cccccc;">&#xa0;};</span>
      </div>
      <div>
        <span style="color: #cccccc;">&#xa0;</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+///&lt; org.quic.camera.CCStats section</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+static CHIVENDORTAGDATA g_VendorTagSectionCCStats[] =</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+{</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;{ &quot;HasFlicker&quot;, &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;TYPE_BYTE, &#xa0;&#xa0;1 &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;},</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+ &#xa0;&#xa0;&#xa0;{ &quot;IsNullFlicker&quot;, &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;TYPE_BYTE, &#xa0;&#xa0;1 &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;},</span>
      </div>
      <div>
        <span style="color: #b5cea8;">+};</span>
      </div>
    </div>
  </body>
</html>
</richcontent>
</node>
</node>
</map>
