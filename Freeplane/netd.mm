<map version="freeplane 1.11.5">
<!--To view this file, download free mind mapping software Freeplane from https://www.freeplane.org -->
<node TEXT="netd" FOLDED="false" ID="ID_107805750" CREATED="1714203830563" MODIFIED="1714203843194" BACKGROUND_COLOR="#0099ff" STYLE="narrow_hexagon" UNIFORM_SHAPE="true" MAX_WIDTH="55.83837 pt" MIN_WIDTH="55.83837 pt" VGAP_QUANTITY="12.75 pt">
<font SIZE="10"/>
<hook NAME="MapStyle">
    <properties show_icon_for_attributes="true" edgeColorConfiguration="#808080ff,#000000ff,#ff0033ff,#009933ff,#3333ffff,#ff6600ff,#cc00ccff,#ffbf00ff,#00ff99ff,#0099ffff,#996600ff,#000000ff,#cc0066ff,#33ff00ff,#ff9999ff,#0000ccff,#cccc00ff,#0099ccff,#006600ff,#ff00ccff,#00cc00ff,#0066ccff,#00ffffff" show_note_icons="true" associatedTemplateLocation="template:/BigMap.mm" fit_to_viewport="false"/>

<map_styles>
<stylenode LOCALIZED_TEXT="styles.root_node" STYLE="oval" UNIFORM_SHAPE="true" VGAP_QUANTITY="24 pt" TEXT_SHORTENED="true">
<font SIZE="24"/>
<stylenode LOCALIZED_TEXT="styles.predefined" POSITION="bottom_or_right" STYLE="bubble">
<font SIZE="9"/>
<stylenode LOCALIZED_TEXT="default" ID="ID_1273250224" ICON_SIZE="12 pt" FORMAT_AS_HYPERLINK="false" COLOR="#000000" STYLE="bubble" SHAPE_VERTICAL_MARGIN="0 pt" NUMBERED="false" FORMAT="STANDARD_FORMAT" TEXT_ALIGN="CENTER" MAX_WIDTH="90 pt" MIN_WIDTH="90 pt" VGAP_QUANTITY="2 pt" BORDER_WIDTH_LIKE_EDGE="false" BORDER_WIDTH="1 px" BORDER_COLOR_LIKE_EDGE="true" BORDER_COLOR="#808080" BORDER_DASH_LIKE_EDGE="false" BORDER_DASH="SOLID">
<arrowlink SHAPE="LINEAR_PATH" COLOR="#000000" WIDTH="2" TRANSPARENCY="200" DASH="" FONT_SIZE="9" FONT_FAMILY="SansSerif" DESTINATION="ID_1273250224" STARTINCLINATION="100.5 pt;0 pt;" ENDINCLINATION="100.5 pt;6.75 pt;" STARTARROW="DEFAULT" ENDARROW="DEFAULT"/>
<font NAME="Arial" SIZE="9" BOLD="true" STRIKETHROUGH="false" ITALIC="false"/>
<edge STYLE="bezier" COLOR="#808080" WIDTH="3" DASH="SOLID"/>
<richcontent TYPE="DETAILS" CONTENT-TYPE="plain/auto"/>
<richcontent TYPE="NOTE" CONTENT-TYPE="plain/auto"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.details" TEXT_ALIGN="LEFT">
<font SIZE="11" BOLD="false"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.attributes" COLOR="#000000" BACKGROUND_COLOR="#ffffff">
<font SIZE="9" BOLD="false"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.note" COLOR="#000000" BACKGROUND_COLOR="#ffffff" TEXT_ALIGN="LEFT">
<font BOLD="false"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.floating">
<edge STYLE="hide_edge"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.selection" BACKGROUND_COLOR="#33ff00" BORDER_COLOR_LIKE_EDGE="false" BORDER_COLOR="#4e85f8"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.user-defined" POSITION="bottom_or_right" STYLE="bubble">
<font SIZE="9"/>
<stylenode LOCALIZED_TEXT="styles.important" ID="ID_1358928635">
<icon BUILTIN="yes"/>
<arrowlink COLOR="#0000ff" TRANSPARENCY="255" DESTINATION="ID_1358928635"/>
<edge COLOR="#0000cc"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.flower" COLOR="#ffffff" BACKGROUND_COLOR="#255aba" STYLE="oval" TEXT_ALIGN="CENTER" BORDER_WIDTH_LIKE_EDGE="false" BORDER_WIDTH="22 pt" BORDER_COLOR_LIKE_EDGE="false" BORDER_COLOR="#f9d71c" BORDER_DASH_LIKE_EDGE="false" BORDER_DASH="CLOSE_DOTS"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.AutomaticLayout" POSITION="bottom_or_right" STYLE="bubble">
<font SIZE="9"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level.root" COLOR="#000000" STYLE="oval" UNIFORM_SHAPE="true" MAX_WIDTH="120 pt" MIN_WIDTH="120 pt">
<font SIZE="24" ITALIC="true"/>
<edge STYLE="bezier" WIDTH="3"/>
</stylenode>
</stylenode>
</stylenode>
</map_styles>
</hook>
<hook NAME="accessories/plugins/AutomaticLayout.properties" VALUE="ALL"/>
<hook NAME="AutomaticEdgeColor" COUNTER="0" RULE="FOR_COLUMNS"/>
<node TEXT="netd.rc" POSITION="bottom_or_right" ID="ID_1782266154" CREATED="1714203857205" MODIFIED="1715040978059"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      service netd /system/bin/netd
    </p>
    <p>
      &#xa0;&#xa0;&#xa0;&#xa0;class main
    </p>
    <p>
      &#xa0;&#xa0;&#xa0;&#xa0;user root
    </p>
    <p>
      &#xa0;&#xa0;&#xa0;&#xa0;group root net_admin
    </p>
  </body>
</html></richcontent>
</node>
<node TEXT="Soft AP" POSITION="top_or_left" ID="ID_501711047" CREATED="1715041182905" MODIFIED="1715041202530">
<node TEXT="AP" ID="ID_1886239766" CREATED="1715041014178" MODIFIED="1715041212988" HGAP_QUANTITY="102.5 pt" VSHIFT_QUANTITY="66 pt"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      AP作为基站设备,起着连
    </p>
    <p>
      接其他无线设备到有线网的作用,相当于有线网络
    </p>
    <p>
      中的HUB与交换机
    </p>
  </body>
</html></richcontent>
</node>
<node TEXT="hostapd" ID="ID_718501134" CREATED="1715041353138" MODIFIED="1715041387108"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      这是一个运行在用户空
    </p>
    <p>
      间的用于AP和认证服务器的守护进程。它实现了
    </p>
    <p>
      IEEE 802.11相关的接入管理、IEEE
    </p>
    <p>
      802.1X/WPA/WPA2/EAP认证、RADIUS客户端、
    </p>
    <p>
      EAP服务器和RADIUS认证服务器
    </p>
  </body>
</html></richcontent>
<node TEXT="fwReloadSoftap" ID="ID_269052178" CREATED="1715041486978" MODIFIED="1715041678300"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      为Wi-Fi加载不同的固件
    </p>
    <p>
      SoftapController.cpp::fwReloadSoftap
    </p>
    <p>
      fwpath = (char*)wifi_get_fw_path(WIFI_GET_FW_PATH_STA);
    </p>
    <p>
      
    </p>
    <p>
      // 通过往/sys/module/wlan/parameters/fwpath文件中写入固件名
    </p>
    <p>
      // 触发驱动去加载对应的固件
    </p>
    <p>
      ret = wifi_change_fw_path((const char *)fwpath);
    </p>
    <p>
      ......
    </p>
    <p>
      return ret;
    </p>
  </body>
</html></richcontent>
<node TEXT="WIFI_GET_FW_PATH_AP" ID="ID_398726881" CREATED="1715041721737" MODIFIED="1715041768964"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      代表Soft AP功能的固件,其对应的文件位置由WIFI_DRIVER_FW_PATH_AP宏表达
    </p>
  </body>
</html></richcontent>
</node>
<node TEXT="WIFI_GET_FW_PATH_P2P" ID="ID_514910178" CREATED="1715041790873" MODIFIED="1715041841157"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      :代表P2P功能的固件,其对应的文件位置由WIFI_DRIVER_FW_PATH_P2P宏表达
    </p>
  </body>
</html></richcontent>
</node>
<node TEXT="WIFI_GET_FW_PATH_STA" ID="ID_559263323" CREATED="1715041876090" MODIFIED="1715041909204"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      :代表Station功能的固件,其对应的文件位置由WIFI_DRIVER_FW_PATH_STA宏表达
    </p>
  </body>
</html></richcontent>
</node>
</node>
<node TEXT="setSoftap" ID="ID_1104388037" CREATED="1715041977418" MODIFIED="1715042139078"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      SoftapController.cpp::setSoftap
    </p>
    <p>
      if (argc &gt; 3) {
    </p>
    <p>
      ssid = argv[3];
    </p>
    <p>
      } else {
    </p>
    <p>
      ssid = (char *)&quot;AndroidAP&quot;; // SSID即接入点的名称
    </p>
    <p>
      }
    </p>
    <p>
      asprintf(&amp;wbuf,&quot;interface=%s\ndriver=nl80211\nctrl_interface=&quot;&quot;/data/misc/wifi/hostapd\nssid=%s\nchannel=6\nieee80
    </p>
    <p>
      iface, ssid);
    </p>
    <p>
      if (argc &gt; 4) { // 判断AP的加密类型
    </p>
    <p>
      if (!strcmp(argv[4], &quot;wpa-psk&quot;)) {
    </p>
    <p>
      generatePsk(ssid, argv[5], psk_str);
    </p>
    <p>
      asprintf(&amp;fbuf, &quot;%swpa=1\nwpa_pair wise=TKIPCCMP\nwpa_psk=%s\n&quot;,wbuf, psk_str);
    </p>
    <p>
      } else if (!strcmp(argv[4], &quot;wpa2-psk&quot;)) {
    </p>
    <p>
      generatePsk(ssid, argv[5], psk_str);
    </p>
    <p>
      asprintf(&amp;fbuf,&quot;%swpa=2\nrsn_pair wise=CCMP\nwpa_psk=%s\n&quot;,wbuf, psk_str);
    </p>
    <p>
      } else if (!strcmp(argv[4], &quot;open&quot;)) {
    </p>
    <p>
      asprintf(&amp;fbuf, &quot;%s&quot;, wbuf);
    </p>
    <p>
      }
    </p>
    <p>
      } ......
    </p>
    <p>
      // HOSTAPD_CONF_FILE指向/data/misc/wifi/hostapd.conf文件
    </p>
    <p>
      fd = open(HOSTAPD_CONF_FILE, O_CREAT | O_TRUNC| O_WRONLY, 0660);
    </p>
    <p>
      ......
    </p>
    <p>
      if (write(fd, fbuf, strlen(fbuf)) &lt; 0) {
    </p>
    <p>
      ALOGE(&quot;Cannot write to \&quot;%s\&quot;: %s&quot;,HOSTAPD_CONF_FILE, strerror(errno));
    </p>
    <p>
      ret = -1;
    </p>
    <p>
      }
    </p>
    <p>
      return ret;
    </p>
  </body>
</html></richcontent>
<node TEXT="hostapd.conf" ID="ID_1321354828" CREATED="1715042199850" MODIFIED="1715042397587"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      android/device/qcom/wlan/bengal/hostapd.conf
    </p>
  </body>
</html></richcontent>
</node>
</node>
<node TEXT="startap" ID="ID_1380905010" CREATED="1715042426369" MODIFIED="1715042457525"><richcontent TYPE="DETAILS">
<html>
  <head>
    
  </head>
  <body>
    <p>
      启动hostapd进程
    </p>
  </body>
</html></richcontent>
</node>
</node>
<node TEXT="Station" ID="ID_1561607149" CREATED="1715064071017" MODIFIED="1715064119521"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      Station代表配备无线网络接口的设备,如手机、笔记本等
    </p>
  </body>
</html></richcontent>
</node>
</node>
<node TEXT="NAT" POSITION="bottom_or_right" ID="ID_1681649700" CREATED="1715042915601" MODIFIED="1715043337149"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      Network Address Translation
    </p>
    <p>
      //更改所有来自192.168.1.0/24的数据包的源IP地址为1.2.3.4:
    </p>
    <p>
      iptables-t nat-A POSTROUTING-s 192.168.1.0/24-o eth0 -j SNAT--to 1.2.3.4
    </p>
    <p>
      //更改所有来自192.168.1.0/24的数据包的目的IP地址为1.2.3.4:
    </p>
    <p>
      iptables-t nat-A PREROUTING-s 192.168.1.0/24-i eth1-j DNAT--to 1.2.3.4
    </p>
  </body>
</html></richcontent>
<node TEXT="SNAT" ID="ID_459094149" CREATED="1715042995817" MODIFIED="1715042999636"/>
<node TEXT="DNAT" ID="ID_489476380" CREATED="1715043004706" MODIFIED="1715043016393"/>
<node TEXT="iptables-&gt;nat" ID="ID_294602954" CREATED="1715043060953" MODIFIED="1715043077754">
<node TEXT="PREROUTING" ID="ID_232025356" CREATED="1715043101298" MODIFIED="1715043104361"/>
<node TEXT="POSTROUTING" ID="ID_438250141" CREATED="1715043248112" MODIFIED="1715043251512"/>
<node TEXT="OUTPUT" ID="ID_1064445310" CREATED="1715043269265" MODIFIED="1715043272361"/>
</node>
</node>
<node TEXT="tty" POSITION="top_or_left" ID="ID_123067542" CREATED="1715043569369" MODIFIED="1715043574504">
<node TEXT="/dev/ttySn" ID="ID_982838573" CREATED="1715046078799" MODIFIED="1715046145595"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      串行端口终端
    </p>
  </body>
</html></richcontent>
</node>
<node TEXT="/dev/ptmx,/dev/pts/" ID="ID_702672906" CREATED="1715046185839" MODIFIED="1715046228978"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      master设备命名为/dev/ptmx,而slave设备则对应/dev/pts/
    </p>
  </body>
</html></richcontent>
</node>
<node TEXT="/dev/ttyN(N 1~64)/dev/console" ID="ID_1527208633" CREATED="1715046259648" MODIFIED="1715046334018"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      /dev/tty0代表当前使用的终端,而/dev/console一般指向这个终端
    </p>
  </body>
</html></richcontent>
</node>
</node>
<node TEXT="pppP" POSITION="bottom_or_right" ID="ID_840957209" CREATED="1715043580290" MODIFIED="1715046652634"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      pppd(PPP Daemon的缩写)是运行PPP协议的后台进程。它和Kernel中的PPP驱动联动,以完成在直连线路(DSL、拨号网络)上建立IP通信链路的工作。
    </p>
  </body>
</html></richcontent>
<node TEXT="PPP" ID="ID_1140098509" CREATED="1715046569975" MODIFIED="1715046590899"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      PPP(Point-to-Point Protocol,点对点协议)是为在同等单元之间传输数据包这样的简单链
    </p>
    <p>
      路设计的链路层协议。这种链路提供全双工操作,并按照顺序传递数据包。
    </p>
  </body>
</html></richcontent>
</node>
</node>
<node TEXT="ndc" POSITION="top_or_left" ID="ID_1020622656" CREATED="1715043732505" MODIFIED="1715043773659"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      监视Netd中发生的事情
    </p>
    <p>
      支持通过命令行发送命令给Netd去执行
    </p>
  </body>
</html></richcontent>
</node>
<node TEXT="USB Tether" POSITION="bottom_or_right" ID="ID_1885835523" CREATED="1715046877567" MODIFIED="1715046885448">
<node TEXT="RNDIS" ID="ID_985554573" CREATED="1715046903079" MODIFIED="1715157172935"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      RNDIS(Remote Network Driver Interface Specification)是微软公司的,主要用于Windows平台中USB网络设备的驱动开发。
    </p>
    <p>
      当手机通过USB连接到主机(主机一般运行Windows系统)后,如果要启用USB绑定,必须要把手机的USB设置成RNDIS 这样,主机上的OS就能识别到一个新的网
    </p>
    <p>
      卡。然后用户就可以选择使用它来开展网络操作。
    </p>
  </body>
</html></richcontent>
</node>
<node TEXT="DHCP" ID="ID_207339858" CREATED="1715046913247" MODIFIED="1715047295003"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      DHCP(Dynamic Host Configuration Protocol,动态主机配置协议)
    </p>
  </body>
</html></richcontent>
<node TEXT="DNSmasq" ID="ID_912459616" CREATED="1715047397279" MODIFIED="1715047745595"><richcontent TYPE="DETAILS">
<html>
  <head>
    
  </head>
  <body>
    <p>
      DNSmasq是一个用于配置DNS和DHCP的工具,小巧且方便,适用于小型网络,它提供了DNS功能和可选择的DHCP功能。它服务只在本地适用的域名
    </p>
  </body>
</html></richcontent>
</node>
</node>
<node TEXT="rndis0" ID="ID_197085726" CREATED="1715047882230" MODIFIED="1715047975641"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      添加需要Tether的接口TetherController.cpp::tetherInterface
    </p>
    <p>
      int TetherController ::tetherInterface(const char*interface) {
    </p>
    <p>
      mInterfaces-&gt;push_back(strdup(interface));
    </p>
    <p>
      // 把需要interface名字保存到一个链表即可
    </p>
    <p>
      return 0;
    </p>
    <p>
      }
    </p>
  </body>
</html></richcontent>
</node>
<node TEXT="startTethering" ID="ID_456432520" CREATED="1715048284678" MODIFIED="1715048460971"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      主要功能就是配置dnsmasq的启动参数并启动它。
    </p>
    <p>
      dnsmasq\
    </p>
    <p>
      --keep-in-foreground\#前台运行
    </p>
    <p>
      --no-resolv\#不解析/etc/resolv.conf,该文件记录域名和dns服务器的一些信息
    </p>
    <p>
      --no-poll\#不关注/etc/resolv.conf文件的变化
    </p>
    <p>
      --dhcp-option-force=43,ANDROID_METERED\#强制的dhcp选项。客户端和dnsmasq交互时,首先会获取dhcp服务器的一些配置信息。43是DHCP协议中定义的option的一种,代表vendor specific infomation该选项说明vendor specifi information就是ANDROID_METERED
    </p>
    <p>
      --pid-file\#指定dnsmasq记录自己进程id(pid)到某个文件。默认是/var/run/dnsmasq.pid
    </p>
    <p>
      --dhcp-range=192.168.1.2 192.168.1.100 1h\#该选项开启dnsmasq的dhcp服务功能。分配的IP地址位于192.168.1.2和192.168.1.100之间。1h代表租约时间为1小时。租约时间即某IP地址可以被DHCP客户端使用的时间。如果超过租约时间,dnsmasq必须为该客户端重新分配IP
    </p>
  </body>
</html></richcontent>
</node>
</node>
<node TEXT="iptables" POSITION="top_or_left" ID="ID_677200261" CREATED="1715050220360" MODIFIED="1715157042434">
<node TEXT=" Filter Table" ID="ID_477027249" CREATED="1715050351792" MODIFIED="1715157121175"/>
<node TEXT="NAT table" ID="ID_1046248047" CREATED="1715050377056" MODIFIED="1715157141215"/>
<node TEXT="Mangle table" ID="ID_650615563" CREATED="1715050403160" MODIFIED="1715157149887"/>
<node TEXT="Raw table" ID="ID_1574769160" CREATED="1715050424800" MODIFIED="1715050668579"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      Iptable’s Raw table is for configuration excemptions. Raw table has the following built-in chains.
    </p>
    <ul>
      <li>
        PREROUTING chain
      </li>
      <li>
        OUTPUT chain
      </li>
    </ul>
  </body>
</html></richcontent>
</node>
<node TEXT="IPTABLES RULES" ID="ID_1385619300" CREATED="1715051041744" MODIFIED="1715157158311"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      The rules in the iptables –list command output contains the following fields:
    </p>
    <ul>
      <li>
        num – Rule number within the particular chain
      </li>
      <li>
        target – Special target variable that we discussed above
      </li>
      <li>
        prot – Protocols. tcp, udp, icmp, etc.,
      </li>
      <li>
        opt – Special options for that specific rule.
      </li>
      <li>
        source – Source ip-address of the packet
      </li>
      <li>
        destination – Destination ip-address for the packet
      </li>
    </ul>
  </body>
</html></richcontent>
</node>
</node>
<node TEXT="TCPDUMP" POSITION="bottom_or_right" ID="ID_1180013020" CREATED="1715051935400" MODIFIED="1715051961202"><richcontent TYPE="DETAILS">
<html>
  <head>
    
  </head>
  <body>
    <p>
      tcpdump command is also called as packet analyzer.
    </p>
  </body>
</html></richcontent>
<node TEXT="tcpdump -i" ID="ID_1058288665" CREATED="1715051990255" MODIFIED="1715052030794"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      When you execute tcpdump command without any option, it will capture all the packets flowing through all the interfaces. -i option with tcpdump command, allows you to filter on a particular ethernet interface.
    </p>
  </body>
</html></richcontent>
<node TEXT="tcpdump -i eth1" ID="ID_596520553" CREATED="1715052213727" MODIFIED="1715052227215"/>
</node>
<node TEXT="tcpdump -c" ID="ID_1929715176" CREATED="1715052157631" MODIFIED="1715052203890"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      When you execute tcpdump command it gives packets until you cancel the tcpdump command. Using -c option you can specify the number of packets to capture.
    </p>
  </body>
</html></richcontent>
<node TEXT="tcpdump -c 2 -i eth0" ID="ID_824791765" CREATED="1715052250919" MODIFIED="1715052253455"/>
</node>
<node TEXT="tcpdump -A" ID="ID_135337623" CREATED="1715052430511" MODIFIED="1715052447979"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      The following tcpdump syntax prints the packet in ASCII.
    </p>
  </body>
</html></richcontent>
<node TEXT="tcpdump -A -i eth0" ID="ID_1631763818" CREATED="1715052462391" MODIFIED="1715052464855"/>
</node>
<node TEXT="tcpdump -XX" ID="ID_805540125" CREATED="1715052485927" MODIFIED="1715052540809"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      &#xa0;tcpdump provides a way to print packets in both ASCII and HEX format.
    </p>
  </body>
</html></richcontent>
<node TEXT="tcpdump -XX -i eth0" ID="ID_578969390" CREATED="1715052493623" MODIFIED="1715052507767"/>
</node>
<node TEXT=" tcpdump -w" ID="ID_1444536008" CREATED="1715053596782" MODIFIED="1715053624250"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      tcpdump allows you to save the packets to a file, and later you can use the packet file for further analysis.
    </p>
  </body>
</html></richcontent>
<node TEXT="tcpdump -w 08232010.pcap -i eth0" ID="ID_1581340489" CREATED="1715053639382" MODIFIED="1715053642102"/>
</node>
<node TEXT="tcpdump -r" ID="ID_1134722902" CREATED="1715053669007" MODIFIED="1715053713890"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      You can read the captured pcap file and view the packets for analysis
    </p>
  </body>
</html></richcontent>
<node TEXT="tcpdump -tttt -r data.pcap" ID="ID_255586007" CREATED="1715053729783" MODIFIED="1715053734815"/>
</node>
<node TEXT="tcpdump -n" ID="ID_465885095" CREATED="1715053766598" MODIFIED="1715053798065"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      Capture packets with IP address
    </p>
  </body>
</html></richcontent>
<node TEXT=" tcpdump -n -i eth0" ID="ID_1669528842" CREATED="1715053813446" MODIFIED="1715053816510"/>
</node>
<node TEXT="tcpdump -tttt" ID="ID_1696029519" CREATED="1715053831879" MODIFIED="1715053859809"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      Capture packets with proper readable timestamp
    </p>
  </body>
</html></richcontent>
<node TEXT="tcpdump -n -tttt -i eth0" ID="ID_399843712" CREATED="1715053872326" MODIFIED="1715053879438"/>
</node>
<node TEXT="tcpdump  greater" ID="ID_1168918759" CREATED="1715060190563" MODIFIED="1715060238503"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      You can receive only the packets greater than n number of bytes using a filter ‘greater’ through tcpdump command
    </p>
  </body>
</html></richcontent>
<node TEXT="tcpdump -w g_1024.pcap greater 1024" ID="ID_1302149742" CREATED="1715060213098" MODIFIED="1715060215978"/>
</node>
<node TEXT="fddi, tr, wlan, ip, ip6, arp, rarp, decnet, tcp and udp" ID="ID_1584148781" CREATED="1715060294435" MODIFIED="1715060322774"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      You can receive the packets based on the protocol type. You can specify one of these protocols — fddi, tr, wlan, ip, ip6, arp, rarp, decnet, tcp and udp.
    </p>
  </body>
</html></richcontent>
<node TEXT="tcpdump -i eth0 arp" ID="ID_725387349" CREATED="1715060333939" MODIFIED="1715060336547"/>
</node>
<node TEXT="tcpdump  less" ID="ID_599026309" CREATED="1715060359339" MODIFIED="1715060393118"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      You can receive only the packets lesser than n number of bytes using a filter ‘less’ through tcpdump command
    </p>
  </body>
</html></richcontent>
<node TEXT="tcpdump -w l_1024.pcap  less 1024" ID="ID_634792449" CREATED="1715060363523" MODIFIED="1715060366603"/>
</node>
<node TEXT=" tcpdump  port" ID="ID_1207805229" CREATED="1715060495914" MODIFIED="1715060570144"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <h3>
      <span style="font-weight: normal; font-size: 12pt;">Receive packets flows on a particular port using tcpdump port</span>
    </h3>
  </body>
</html></richcontent>
<node TEXT=" tcpdump -i eth0 port 22" ID="ID_969624039" CREATED="1715060498771" MODIFIED="1715060501811"/>
</node>
<node TEXT=" tcpdump  dst  and port" ID="ID_1351530502" CREATED="1715060598883" MODIFIED="1715060655021"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      <span style="font-size: 12pt;">Capture packets for particular destination IP and Port</span>
    </p>
  </body>
</html></richcontent>
<node TEXT=" tcpdump -w xpackets.pcap -i eth0 dst 10.181.140.216 and port 22" ID="ID_927793360" CREATED="1715060602339" MODIFIED="1715060608019"/>
</node>
<node TEXT="not  and  or" ID="ID_475552365" CREATED="1715060825434" MODIFIED="1715060880237"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      In tcpdump command, you can give “and”, “or” and “not” condition to filter the packets accordingly
    </p>
  </body>
</html></richcontent>
<node TEXT="tcpdump -i eth0 not arp and not rarp" ID="ID_52126250" CREATED="1715060831155" MODIFIED="1715060834794"/>
</node>
</node>
</node>
</map>
