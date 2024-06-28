<map version="freeplane 1.11.5">
<!--To view this file, download free mind mapping software Freeplane from https://www.freeplane.org -->
<node TEXT=" wpa_supplicant lib 流程" FOLDED="false" ID="ID_696401721" CREATED="1610381621824" MODIFIED="1719210426058" STYLE="oval">
<font SIZE="18"/>
<hook NAME="MapStyle" zoom="0.912">
    <properties edgeColorConfiguration="#808080ff,#ff0000ff,#0000ffff,#00ff00ff,#ff00ffff,#00ffffff,#7c0000ff,#00007cff,#007c00ff,#7c007cff,#007c7cff,#7c7c00ff" fit_to_viewport="false" associatedTemplateLocation="template:/standard-1.6.mm"/>

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
<hook NAME="AutomaticEdgeColor" COUNTER="7" RULE="ON_BRANCH_CREATION"/>
<node TEXT="wpa_driver_nl80211_driver_cmd" POSITION="bottom_or_right" ID="ID_1161528931" CREATED="1719193556440" MODIFIED="1719193585287">
<edge COLOR="#ff0000"/>
<richcontent TYPE="DETAILS">
<html>
  <head>
    
  </head>
  <body>
    <p>
      LA.VENDOR.13.2.1.r1/LINUX/android/hardware/qcom/wlan/qcwcn/wpa_supplicant_8_lib/driver_cmd_nl80211.c
    </p>
  </body>
</html>
</richcontent>
<node TEXT="MACADDR" ID="ID_1216864572" CREATED="1719193612566" MODIFIED="1719193733049"><richcontent TYPE="DETAILS">
<html>
  <head>
    
  </head>
  <body>
    <pre>u8 macaddr[ETH_ALEN] = {};

ret = linux_get_ifhwaddr(drv-&gt;global-&gt;ioctl_sock, bss-&gt;ifname, macaddr);
f (!ret)
    ret = os_snprintf(buf, buf_len,
    &quot;Macaddr = &quot; MAC_ADDR_STR &quot;\n&quot;, MAC_ADDR_ARRAY(macaddr));</pre>
  </body>
</html>
</richcontent>
</node>
</node>
<node TEXT="wpa_supplicant : getMacAddressInternal" POSITION="top_or_left" ID="ID_570691347" CREATED="1719195015353" MODIFIED="1719195358894">
<edge COLOR="#0000ff"/>
<richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      LA.QSSI.14.0.r1/LINUX/android/external/wpa_supplicant_8/wpa_supplicant/aidl/sta_iface.cpp
    </p>
    <p>
      constexpr char kGetMacAddress[] = &quot;MACADDR&quot;;
    </p>
    <p>
      
    </p>
    <pre>std::pair&lt;std::vector&lt;uint8_t&gt;, ndk::ScopedAStatus&gt;
StaIface::getMacAddressInternal()
{
&#x9;struct wpa_supplicant *wpa_s = retrieveIfacePtr();
&#x9;std::vector&lt;char&gt; cmd(
&#x9;&#x9;kGetMacAddress, kGetMacAddress + sizeof(kGetMacAddress));
&#x9;char driver_cmd_reply_buf[4096] = {};
&#x9;int ret = wpa_drv_driver_cmd(
&#x9;&#x9;wpa_s, cmd.data(), driver_cmd_reply_buf,
&#x9;&#x9;sizeof(driver_cmd_reply_buf));
&#x9;// Reply is of the format: &quot;Macaddr = XX:XX:XX:XX:XX:XX&quot;
&#x9;std::string reply_str = driver_cmd_reply_buf;
&#x9;if (ret &lt; 0 || reply_str.empty() ||
&#x9;&#x9;reply_str.find(&quot;=&quot;) == std::string::npos) {
&#x9;&#x9;return {std::vector&lt;uint8_t&gt;(),
&#x9;&#x9;&#x9;createStatus(SupplicantStatusCode::FAILURE_UNKNOWN)};
&#x9;}
&#x9;// Remove all whitespace first and then split using the delimiter &quot;=&quot;.
&#x9;reply_str.erase(
&#x9;&#x9;remove_if(reply_str.begin(), reply_str.end(), isspace),
&#x9;&#x9;reply_str.end());
&#x9;std::string mac_addr_str =
&#x9;&#x9;reply_str.substr(reply_str.find(&quot;=&quot;) + 1, reply_str.size());
&#x9;std::vector&lt;uint8_t&gt; mac_addr(6);
&#x9;if (hwaddr_aton(mac_addr_str.c_str(), mac_addr.data())) {
&#x9;&#x9;return {std::vector&lt;uint8_t&gt;(),
&#x9;&#x9;&#x9;createStatus(SupplicantStatusCode::FAILURE_UNKNOWN)};
&#x9;}
&#x9;return {mac_addr, ndk::ScopedAStatus::ok()};
}</pre>
  </body>
</html>
</richcontent>
<node TEXT="getMacAddress" ID="ID_1741067315" CREATED="1719195085470" MODIFIED="1719281686889"><richcontent TYPE="DETAILS">
<html>
  <head>
    
  </head>
  <body>
    <pre>::ndk::ScopedAStatus StaIface::getMacAddress(
&#x9;std::vector&lt;uint8_t&gt;* _aidl_return)
{
&#x9;return validateAndCall(
&#x9;&#x9;this, SupplicantStatusCode::FAILURE_IFACE_INVALID,
&#x9;&#x9;&amp;StaIface::getMacAddressInternal, _aidl_return);
}</pre>
  </body>
</html>
</richcontent>
</node>
</node>
<node TEXT="CONFIG_CTRL_IFACE_AIDL=y" POSITION="bottom_or_right" ID="ID_254453897" CREATED="1719195721942" MODIFIED="1719195749568">
<edge COLOR="#00ff00"/>
<richcontent TYPE="DETAILS">
<html>
  <head>
    
  </head>
  <body>
    <pre># Add support for Aidl control interface
# Only applicable for Android platforms.</pre>
  </body>
</html>
</richcontent>
<node TEXT="WPA_SUPPLICANT_USE_AIDL=y" ID="ID_296576850" CREATED="1719195753449" MODIFIED="1719195802199"><richcontent TYPE="DETAILS">
<html>
  <head>
    
  </head>
  <body>
    <pre>ifdef CONFIG_CTRL_IFACE_AIDL
WPA_SUPPLICANT_USE_AIDL=y
L_CFLAGS += -DCONFIG_AIDL -DCONFIG_CTRL_IFACE_AIDL
endif</pre>
  </body>
</html>
</richcontent>
<node TEXT="libwpa_aidl" ID="ID_275253926" CREATED="1719196196877" MODIFIED="1719198498610"><richcontent TYPE="DETAILS">
<html>
  <head>
    
  </head>
  <body>
    <pre>ifeq ($(WPA_SUPPLICANT_USE_AIDL), y)
LOCAL_SHARED_LIBRARIES += android.hardware.wifi.supplicant-V2-ndk
LOCAL_SHARED_LIBRARIES += android.system.keystore2-V1-ndk
LOCAL_SHARED_LIBRARIES += libutils libbase
LOCAL_SHARED_LIBRARIES += libbinder_ndk
LOCAL_STATIC_LIBRARIES += libwpa_aidl
LOCAL_VINTF_FRAGMENTS := aidl/android.hardware.wifi.supplicant.xml
ifeq ($(SUPPLICANT_VENDOR_AIDL), y)
LOCAL_SHARED_LIBRARIES += vendor.qti.hardware.wifi.supplicant-V1-ndk
endif
ifeq ($(WIFI_HIDL_UNIFIED_SUPPLICANT_SERVICE_RC_ENTRY), true)
LOCAL_INIT_RC=aidl/android.hardware.wifi.supplicant-service.rc
endif
endif</pre>
  </body>
</html>
</richcontent>
</node>
</node>
</node>
<node TEXT="getMacAddress" POSITION="top_or_left" ID="ID_1320484568" CREATED="1719210485338" MODIFIED="1719223919539">
<edge COLOR="#ff00ff"/>
<richcontent TYPE="DETAILS">
<html>
  <head>
    
  </head>
  <body>
    <pre><span class="c">LA.QSSI.14.0.r1/LINUX/android/packages/modules/Wifi/service/java/com/android/server/wifi/SupplicantStaIfaceHalHidlImpl.java
Makes a callback to HIDL to getMacAddress from supplicant</span>
    </pre>
    <pre>    public String getMacAddress(@NonNull String ifaceName) {
        synchronized (mLock) {
            final String methodStr = &quot;getMacAddress&quot;;
            ISupplicantStaIface iface = checkSupplicantStaIfaceAndLogFailure(ifaceName, methodStr);
            if (iface == null) return null;
            Mutable&lt;String&gt; gotMac = new Mutable&lt;&gt;();
            try {
                iface.getMacAddress((SupplicantStatus status,
                        byte[/* 6 */] macAddr) -&gt; {
                    if (checkStatusAndLogFailure(status, methodStr)) {
                        gotMac.value = NativeUtil.macAddressFromByteArray(macAddr);
                    }
                });
            } catch (RemoteException e) {
                handleRemoteException(e, methodStr);
            }
            return gotMac.value;
        }
    }</pre>
  </body>
</html>
</richcontent>
<node TEXT="getFactoryMacAddresses" ID="ID_1947173474" CREATED="1719280281566" MODIFIED="1719280388520"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <pre>LA.QSSI.14.0.r1/LINUX/android/packages/modules/Wifi/framework/java/android/net/wifi/WifiManager.java
public String[] getFactoryMacAddresses() {
        try {
            return mService.getFactoryMacAddresses();
        } catch (RemoteException e) {
            throw e.rethrowFromSystemServer();
        }
    }</pre>
  </body>
</html>
</richcontent>
<node TEXT="public String[] getFactoryMacAddresses()" ID="ID_1507064809" CREATED="1719280620192" MODIFIED="1719280671649"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <p>
      LA.QSSI.14.0.r1/LINUX/android/packages/modules/Wifi/service/java/com/android/server/wifi/WifiServiceImpl.java
    </p>
    <pre>    public String[] getFactoryMacAddresses() {
        final int uid = Binder.getCallingUid();
        if (!mWifiPermissionsUtil.checkNetworkSettingsPermission(uid)) {
            throw new SecurityException(&quot;App not allowed to get Wi-Fi factory MAC address &quot;
                    + &quot;(uid = &quot; + uid + &quot;)&quot;);
        }
        String result = mWifiThreadRunner.call(
                () -&gt; mActiveModeWarden.getPrimaryClientModeManager().getFactoryMacAddress(),
                null);
        // result can be empty array if either: WifiThreadRunner.call() timed out, or
        // ClientModeImpl.getFactoryMacAddress() returned null.
        // In this particular instance, we don't differentiate the two types of nulls.
        if (result == null) {
            return new String[0];
        }
        return new String[]{result};
    }</pre>
  </body>
</html>
</richcontent>
<node TEXT="getFactoryMacAddress" ID="ID_489039636" CREATED="1719283987199" MODIFIED="1719286893942"><richcontent TYPE="DETAILS">
<html>
  <head>
    
  </head>
  <body>
    <p>
      LA.VENDOR.13.2.1.r1/LINUX/android/packages/modules/Wifi/service/java/com/android/server/wifi/ConcreteClientModeManager.java
    </p>
    <pre>     public String getFactoryMacAddress() {
          return getClientMode().getFactoryMacAddress();
      }</pre>
  </body>
</html>
</richcontent>
<node TEXT="getFactoryMacAddress" ID="ID_1068582502" CREATED="1719284135776" MODIFIED="1719286966850"><richcontent TYPE="DETAILS">
<html>
  <head>
    
  </head>
  <body>
    <p>
      LA.QSSI.14.0.r1/LINUX/android/packages/modules/Wifi/service/java/com/android/server/wifi/ClientModeImpl.java
    </p>
    <pre><span class="c"> Gets the factory MAC address of wlan0 (station interface).</span></pre>
    <pre>    public String getFactoryMacAddress() {
        MacAddress factoryMacAddress = retrieveFactoryMacAddressAndStoreIfNecessary();
        if (factoryMacAddress != null) return factoryMacAddress.toString();

        // For devices with older HAL's (version &lt; 1.3), no API exists to retrieve factory MAC
        // address (and also does not support MAC randomization - needs verson 1.2). So, just
        // return the regular MAC address from the interface.
        if (!mWifiGlobals.isConnectedMacRandomizationEnabled()) {
            Log.w(TAG, &quot;Can't get factory MAC address, return the MAC address&quot;);
            return mWifiNative.getMacAddress(mInterfaceName);
        }
        return null;
    }</pre>
  </body>
</html>
</richcontent>
<node TEXT=" retrieveFactoryMacAddressAndStoreIfNecessary" ID="ID_1696810869" CREATED="1719285245279" MODIFIED="1719285297780"><richcontent TYPE="DETAILS">
<html>
  <head>
    
  </head>
  <body>
    <pre>    private MacAddress retrieveFactoryMacAddressAndStoreIfNecessary() {
        boolean saveFactoryMacInConfigStore =
                mWifiGlobals.isSaveFactoryMacToConfigStoreEnabled();
        if (saveFactoryMacInConfigStore) {
            // Already present, just return.
            String factoryMacAddressStr = mSettingsConfigStore.get(isPrimary()
                    ? WIFI_STA_FACTORY_MAC_ADDRESS : SECONDARY_WIFI_STA_FACTORY_MAC_ADDRESS);
            if (factoryMacAddressStr != null) return MacAddress.fromString(factoryMacAddressStr);
        }
        MacAddress factoryMacAddress = mWifiNative.getStaFactoryMacAddress(mInterfaceName);
        if (factoryMacAddress == null) {
            // the device may be running an older HAL (version &lt; 1.3).
            Log.w(TAG, (isPrimary() ? &quot;Primary&quot; : &quot;Secondary&quot;)
                    + &quot; failed to retrieve factory MAC address&quot;);
            return null;
        }
        if (saveFactoryMacInConfigStore) {
            mSettingsConfigStore.put(isPrimary()
                            ? WIFI_STA_FACTORY_MAC_ADDRESS : SECONDARY_WIFI_STA_FACTORY_MAC_ADDRESS,
                    factoryMacAddress.toString());
            Log.i(TAG, (isPrimary() ? &quot;Primary&quot; : &quot;Secondary&quot;)
                    + &quot; factory MAC address stored in config store: &quot; + factoryMacAddress);
        }
        Log.i(TAG, (isPrimary() ? &quot;Primary&quot; : &quot;Secondary&quot;)
                + &quot; factory MAC address retrieved: &quot; + factoryMacAddress);
        return factoryMacAddress;
    }</pre>
  </body>
</html>
</richcontent>
</node>
</node>
</node>
</node>
</node>
<node TEXT="getMacAddress" ID="ID_840112319" CREATED="1719286593005" MODIFIED="1719286647094"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <pre>Makes a callback to HIDL to getMacAddress from supplicant</pre>
    <p>
      LA.QSSI.14.0.r1/LINUX/android/packages/modules/Wifi/service/java/com/android/server/wifi/WifiNative.java
    </p>
    <pre>public String getMacAddress(@NonNull String ifaceName) {
        return mSupplicantStaIfaceHal.getMacAddress(ifaceName);
    }</pre>
  </body>
</html>
</richcontent>
<node TEXT="getMacAddress" ID="ID_566883290" CREATED="1719223984836" MODIFIED="1719281644306"><richcontent TYPE="DETAILS" HIDDEN="true">
<html>
  <head>
    
  </head>
  <body>
    <pre>LA.QSSI.14.0.r1/LINUX/android/packages/modules/Wifi/service/java/com/android/server/wifi/SupplicantStaIfaceHal.java
    public String getMacAddress(@NonNull String ifaceName) {
        synchronized (mLock) {
            String methodStr = &quot;getMacAddress&quot;;
            if (mStaIfaceHal == null) {
                handleNullHal(methodStr);
                return null;
            }
            return mStaIfaceHal.getMacAddress(ifaceName);
        }
    }</pre>
  </body>
</html></richcontent>
</node>
</node>
</node>
<node TEXT="WifiGlobals" POSITION="top_or_left" ID="ID_131484430" CREATED="1719286968073" MODIFIED="1719287029895">
<edge COLOR="#7c0000"/>
<richcontent TYPE="DETAILS">
<html>
  <head>
    
  </head>
  <body>
    <pre><span class="c"> Global wifi service in-memory state that is not persiste</span></pre>
    <p>
      LA.QSSI.14.0.r1/LINUX/android/packages/modules/Wifi/service/java/com/android/server/wifi/WifiGlobals.java
    </p>
  </body>
</html>
</richcontent>
<node TEXT="isConnectedMacRandomizationEnabled" ID="ID_982800118" CREATED="1719284492524" MODIFIED="1719287038362"><richcontent TYPE="DETAILS">
<html>
  <head>
    
  </head>
  <body>
    <pre><span class="c">Helper method to check if Connected MAC Randomization is supported</span></pre>
    <p>
      LA.QSSI.14.0.r1/LINUX/android/packages/modules/Wifi/service/java/com/android/server/wifi/WifiGlobals.java
    </p>
    <p>
      
    </p>
    <pre>public boolean isConnectedMacRandomizationEnabled() {
         return mContext.getResources().getBoolean(
                  R.bool.config_wifi_connected_mac_randomization_supported);
 }  </pre>
  </body>
</html></richcontent>
</node>
<node TEXT="isSaveFactoryMacToConfigStoreEnabled" ID="ID_103321246" CREATED="1719287062271" MODIFIED="1719287286911"><richcontent TYPE="DETAILS">
<html>
  <head>
    
  </head>
  <body>
    <pre><span class="c">Get whether to use the saved factory MAC address when available</span>
    </pre>
    <pre>mSaveFactoryMacToConfigStoreEnabled = mContext.getResources()
                .getBoolean(R.bool.config_wifiSaveFactoryMacToWifiConfigStore);

    </pre>
    <pre><span class="c">&lt;!-- Set to &quot;true&quot; to always use the factory MAC saved in WifiConfigStore when available.
<a class="l selected" name="368" href="http://192.168.117.122:8080/source/xref/UPQ0090010-T10/LA.QSSI.14.0.r1/LINUX/android/packages/modules/Wifi/service/ServiceWifiResources/res/values/config.xml#368">368 </a>         Set to &quot;false&quot; to get the factory MAC from vendor HAL every time it's needed. --&gt;</span></pre>
    LA.QSSI.14.0.r1/LINUX/android/packages/modules/Wifi/service/ServiceWifiResources/res/values/config.xml
  </body>
</html>
</richcontent>
</node>
</node>
<node TEXT="APP: WifiManager.getFactoryMacAddress()" POSITION="bottom_or_right" ID="ID_778492194" CREATED="1719292406474" MODIFIED="1719292461024">
<edge COLOR="#00007c"/>
<richcontent TYPE="DETAILS">
<html>
  <head>
    
  </head>
  <body>
    <p>
      以下是一个使用 WifiManager.getFactoryMacAddress() 方法的示例：
    </p>
    <pre><code class="language-java">WifiManager wifiManager = (WifiManager) getSystemService(Context.WIFI_SERVICE);
String macAddress = wifiManager.getFactoryMacAddress();</code></pre>
    <p>
      需要注意的是，为了使用这些 API，你的应用程序需要在 AndroidManifest.xml 文件中请求 Wi-Fi 状态权限：
    </p>
    <pre><code class="language-xml">&lt;uses-permission android:name=&quot;android.permission.ACCESS_WIFI_STATE&quot; /&gt;</code></pre>
  </body>
</html>
</richcontent>
</node>
</node>
</map>
