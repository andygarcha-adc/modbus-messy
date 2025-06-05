from enum import Enum
import csv
import time

class ModBusType(Enum) :
    Bit = 0
    Integer = 1
    Integer2 = 2
    Hexadecimal = 3
    FloatingPoint = 4
    Text = 5
    pass

 # ----  VERY LARGE ARRAY  ----
NICKNAMES = {
    'SC1': '_Always_ON',
    'SC2': '_1st_SCAN',
    'SC3': '_SCAN_Clock',
    'SC4': '_10ms_Clock',
    'SC5': '_100ms_Clock',
    'SC6': '_500ms_Clock',
    'SC7': '_1sec_Clock',
    'SC8': '_1min_Clock',
    'SC9': '_1hour_Clock',
    'SC10': '_Mode_Switch',
    'SC11': '_PLC_Mode',
    'SC19': '_PLC Error',
    'SC20': '_I/O Module Error',
    'SC21': '_System Config Error',
    'SC22': '_I/O Config Error',
    'SC23': '_Memory Check Error',
    'SC24': '_Project File Error',
    'SC25': '_Firmware Version Error',
    'SC26': '_Watchdog Timer Error',
    'SC27': '_Lost SDRAM Data',
    'SC28': '_Battery Low Voltage',
    'SC29': '_Battery Replacement',
    'SC30': '_Run Edit Project Error',
    'SC31': '_Sub_CPU_FW_Ver_Error',
    'SC32': '_C2INT_FW_Ver_Error',
    'SC33': '_CPLD Version Error',
    'SC40': '_Division_Error',
    'SC43': '_Out_of_Range',
    'SC44': '_Address_Error',
    'SC46': '_Math_Operation_Error',
    'SC50': '_PLC_Mode_Change_to_STOP',
    'SC51': '_Watchdog_Timer_Reset',
    'SC53': '_RTC_Date_Change',
    'SC54': '_RTC_Date_Change_Error',
    'SC55': '_RTC_Time_Change',
    'SC56': '_RTC_Time_Change_Error',
    'SC60': '_BT_Disable_Pairing',
    'SC61': '_BT_Activate_Pairing',
    'SC62': '_BT_Paired_Devices',
    'SC63': '_BT_Pairing_SW_State',
    'SC64': '_RemotePLC_Enabled',
    'SC65': '_SD_Eject',
    'SC66': '_SD_Delete_All',
    'SC67': '_SD_Copy_System',
    'SC68': '_SD_Ready_To_Use',
    'SC69': '_SD_Write_Status',
    'SC70': '_SD_Error',
    'SC75': '_WLAN_Reset',
    'SC76': '_Sub_CPU_Reset',
    'SC80': '_WLAN_Ready_Flag',
    'SC81': '_WLAN_Error_Flag',
    'SC82': '_WLAN_Connection_Limit',
    'SC83': '_WLAN_IP_Resolved',
    'SC84': '_WLAN_Connected',
    'SC86': '_WLAN_DHCP_Enabled',
    'SC87': '_WLAN_DNS_Success',
    'SC88': '_WLAN_DNS_Error',
    'SC90': '_Port_1_Ready_Flag',
    'SC91': '_Port_1_Error_Flag',
    'SC92': '_Port_1_Connection_Limit',
    'SC93': '_Port_1_IP_Resolved',
    'SC94': '_Port_1_Link_Flag',
    'SC95': '_Port_1_100MBIT_Flag',
    'SC96': '_Port_1_DHCP_Enabled',
    'SC97': '_Port_1_DNS_Success',
    'SC98': '_Port_1_DNS_Error',
    'SC100': '_Port_2_Ready_Flag',
    'SC101': '_Port_2_Error_Flag',
    'SC102': '_Port_3_Ready_Flag',
    'SC103': '_Port_3_Error_Flag',
    'SC111': '_EIP_Con1_ConOnline',
    'SC112': '_EIP_Con1_Error',
    'SC113': '_EIP_Con1_Originator_Run',
    'SC114': '_EIP_Con2_ConOnline',
    'SC115': '_EIP_Con2_Error',
    'SC116': '_EIP_Con2_Originator_Run',
    'SC120': '_Network Time_Request',
    'SC121': '_Network Time_DST',
    'SC122': '_Network Time_Processing',
    'SC123': '_Network Time_Error',
    'SC131': '_Password_Failure_Detect',
    'SC132': '_Password_Locked_Out',
    'SC133': '_Port1_AL_Enabled',
    'SC134': '_Port1_AL_Denied_Flag',
    'SC135': '_WLAN_AL_Enabled',
    'SC136': '_WLAN_AL_Denied_Flag',
    'SC140': '_S0_P1_Ready_Flag',
    'SC141': '_S0_P1_Error_Flag',
    'SC142': '_S0_P2_Ready_Flag',
    'SC143': '_S0_P2_Error_Flag',
    'SC144': '_S1_P1_Ready_Flag',
    'SC145': '_S1_P1_Error_Flag',
    'SC146': '_S1_P2_Ready_Flag',
    'SC147': '_S1_P2_Error_Flag',
    'SC150': '_PTO_Axis1_Ready_Flag',
    'SC151': '_PTO_Axis2_Ready_Flag',
    'SC152': '_PTO_Axis3_Ready_Flag',
    'SC202': '_Fixed_Scan_Mode',
    'SC203': '_Battery_Installed',
    'SC301': '_S0INT_Ready_Flag',
    'SC302': '_S0INT_Error_Flag',
    'SC303': '_S0INT_Reset',
    'SC304': '_S0INT_SD_EJECT',
    'SC305': '_S0INT_SD_Delete_All',
    'SC306': '_S0INT_SD_Copy_System',
    'SC307': '_S0INT_SD_Ready_To_Use',
    'SC309': '_S0INT_IP_Resolved',
    'SC310': '_S0INT_Link_Flag',
    'SC311': '_S0INT_100M_Bit_Flag',
    'SC312': '_S0INT_DHCP_Enabled',
    'SC315': '_S0INT_Application_Flag',
    'SC321': '_S1INT_Ready_Flag',
    'SC322': '_S1INT_Error_Flag',
    'SC323': '_S1INT_Reset',
    'SC324': '_S1INT_SD_EJECT',
    'SC325': '_S1INT_SD_Delete_All',
    'SC326': '_S1INT_SD_Copy_System',
    'SC327': '_S1INT_SD_Ready_To_Use',
    'SC329': '_S1INT_IP_Resolved',
    'SC330': '_S1INT_Link_Flag',
    'SC331': '_S1INT_100M_Bit_Flag',
    'SC332': '_S1INT_DHCP_Enabled',
    'SC335': '_S1INT_Application_Flag',
    'SD1': '_PLC_Error_Code',
    'SD5': '_Firmware_Version_L',
    'SD6': '_Firmware_Version_H',
    'SD7': '_Sub_Firmware_Version_L',
    'SD8': '_Sub_Firmware_Version_H',
    'SD9': '_Scan_Counter',
    'SD10': '_Current_Scan_Time',
    'SD11': '_Minimum_Scan_Time',
    'SD12': '_Maximum_Scan_Time',
    'SD13': '_Fixed_Scan_Time_Setup',
    'SD14': '_Interrupt_Scan_Time',
    'SD19': '_RTC_Year(4 digits)',
    'SD20': '_RTC_Year(2 digits)',
    'SD21': '_RTC_Month',
    'SD22': '_RTC_Day',
    'SD23': '_RTC_Day_of_The_Week',
    'SD24': '_RTC_Hour',
    'SD25': '_RTC_Minute',
    'SD26': '_RTC_Second',
    'SD29': '_RTC_New_Year(4 digits)',
    'SD31': '_RTC_New_Month',
    'SD32': '_RTC_New_Day',
    'SD34': '_RTC_New_Hour',
    'SD35': '_RTC_New_Minute',
    'SD36': '_RTC_New_Second',
    'SD40': '_Port1_Received_Data_Len',
    'SD41': '_Port1_No_Comm_Time',
    'SD42': '_Port1_Rcv_Pkt_High_Cnt',
    'SD50': '_Port2_Received_Data_Len',
    'SD51': '_Port2_No_Comm_Time',
    'SD60': '_Port3_Received_Data_Len',
    'SD61': '_Port3_No_Comm_Time',
    'SD62': '_BT_Paired_Device_Count',
    'SD63': '_SD_Total_Memory_L',
    'SD64': '_SD_Total_Memory_H',
    'SD65': '_SD_Free_Memory_L',
    'SD66': '_SD_Free_Memory_H',
    'SD67': '_SD_Used_Memory_L',
    'SD68': '_SD_Used_Memory_H',
    'SD69': '_SD_Error_Information',
    'SD70': '_SD_Log_File_Number',
    'SD80': '_Port1_IP_Address1',
    'SD81': '_Port1_IP_Address2',
    'SD82': '_Port1_IP_Address3',
    'SD83': '_Port1_IP_Address4',
    'SD84': '_Port1_Subnet_Mask1',
    'SD85': '_Port1_Subnet_Mask2',
    'SD86': '_Port1_Subnet_Mask3',
    'SD87': '_Port1_Subnet_Mask4',
    'SD88': '_Port1_Default_Gateway1',
    'SD89': '_Port1_Default_Gateway2',
    'SD90': '_Port1_Default_Gateway3',
    'SD91': '_Port1_Default_Gateway4',
    'SD101': '_EIP_ModuleStatus',
    'SD102': '_EIP_IdentityStatus',
    'SD103': '_EIP_Con1_NodeStatus',
    'SD104': '_EIP_Con1_GeneralStatus',
    'SD105': '_EIP_Con1_ExtendedStatus',
    'SD106': '_EIP_Con1_LostCount',
    'SD107': '_EIP_Con1_DisConCount',
    'SD108': '_EIP_Con1_No_Comm_Time',
    'SD109': '_EIP_Con2_NodeStatus',
    'SD110': '_EIP_Con2_GeneralStatus',
    'SD111': '_EIP_Con2_ExtendedStatus',
    'SD112': '_EIP_Con2_LostCount',
    'SD113': '_EIP_Con2_DisConCount',
    'SD114': '_EIP_Con2_No_Comm_Time',
    'SD131': '_Password_Failed_Count',
    'SD132': '_Port1_AL_Denied_No1_Cnt',
    'SD133': '_WLAN_AL_Denied_No1_Cnt',
    'SD134': '_Port1_AL_Denied_Count',
    'SD135': '_WLAN_AL_Denied_Count',
    'SD140': '_S0_P1_Received_Data_Len',
    'SD141': '_S0_P1_No_Comm_Time',
    'SD142': '_S0_P2_Received_Data_Len',
    'SD143': '_S0_P2_No_Comm_Time',
    'SD144': '_S1_P1_Received_Data_Len',
    'SD145': '_S1_P1_No_Comm_Time',
    'SD146': '_S1_P2_Received_Data_Len',
    'SD147': '_S1_P2_No_Comm_Time',
    'SD150': '_RemotePLC_Connect_Cnt',
    'SD188': '_Port1_MAC_Address1',
    'SD189': '_Port1_MAC_Address2',
    'SD190': '_Port1_MAC_Address3',
    'SD191': '_Port1_MAC_Address4',
    'SD192': '_Port1_MAC_Address5',
    'SD193': '_Port1_MAC_Address6',
    'SD194': '_WLAN_ST_MAC_Address1',
    'SD195': '_WLAN_ST_MAC_Address2',
    'SD196': '_WLAN_ST_MAC_Address3',
    'SD197': '_WLAN_ST_MAC_Address4',
    'SD198': '_WLAN_ST_MAC_Address5',
    'SD199': '_WLAN_ST_MAC_Address6',
    'SD200': '_WLAN_IP_Address1',
    'SD201': '_WLAN_IP_Address2',
    'SD202': '_WLAN_IP_Address3',
    'SD203': '_WLAN_IP_Address4',
    'SD204': '_WLAN_Subnet_Mask1',
    'SD205': '_WLAN_Subnet_Mask2',
    'SD206': '_WLAN_Subnet_Mask3',
    'SD207': '_WLAN_Subnet_Mask4',
    'SD208': '_WLAN_Default_Gateway1',
    'SD209': '_WLAN_Default_Gateway2',
    'SD210': '_WLAN_Default_Gateway3',
    'SD211': '_WLAN_Default_Gateway4',
    'SD212': '_WLAN_Signal_Strength',
    'SD213': '_WLAN_Connection_Status',
    'SD214': '_WLAN_No_Comm_Time',
    'SD215': '_WLAN_Rcv_Pkt_High_Cnt',
    'SD216': '_WLAN_Connected_Channel',
    'SD217': '_WLAN_Country_Code',
    'SD218': '_WLAN_No_Connect_Status',
    'SD301': '_S0_ModuleId',
    'SD302': '_S0_Major_Version',
    'SD303': '_S0_Minor_Version',
    'SD304': '_S0_Hotfix_Version',
    'SD305': '_S0_Release_Version',
    'SD306': '_S0_CPU_USAGE',
    'SD307': '_S0_MEM_USAGE',
    'SD308': '_S0_ERROR_CODE',
    'SD309': '_S0_SD_TOTAL_MEM_L',
    'SD310': '_S0_SD_TOTAL_MEM_H',
    'SD311': '_S0_SD_FREE_MEM_L',
    'SD312': '_S0_SD_FREE_MEM_H',
    'SD313': '_S0_SD_USED_MEM_L',
    'SD314': '_S0_SD_USED_MEM_H',
    'SD315': '_S0_ETH_IP_Address1',
    'SD316': '_S0_ETH_IP_Address2',
    'SD317': '_S0_ETH_IP_Address3',
    'SD318': '_S0_ETH_IP_Address4',
    'SD319': '_S0_ETH_Subnet_Mask1',
    'SD320': '_S0_ETH_Subnet_Mask2',
    'SD321': '_S0_ETH_Subnet_Mask3',
    'SD322': '_S0_ETH_Subnet_Mask4',
    'SD323': '_S0_ETH_Default_Gateway1',
    'SD324': '_S0_ETH_Default_Gateway2',
    'SD325': '_S0_ETH_Default_Gateway3',
    'SD326': '_S0_ETH_Default_Gateway4',
    'SD327': '_S0_ETH_MAC_Address1',
    'SD328': '_S0_ETH_MAC_Address2',
    'SD329': '_S0_ETH_MAC_Address3',
    'SD330': '_S0_ETH_MAC_Address4',
    'SD331': '_S0_ETH_MAC_Address5',
    'SD332': '_S0_ETH_MAC_Address6',
    'SD333': '_S0_USB_IP_Address1',
    'SD334': '_S0_USB_IP_Address2',
    'SD335': '_S0_USB_IP_Address3',
    'SD336': '_S0_USB_IP_Address4',
    'SD337': '_S0_USB_Subnet_Mask1',
    'SD338': '_S0_USB_Subnet_Mask2',
    'SD339': '_S0_USB_Subnet_Mask3',
    'SD340': '_S0_USB_Subnet_Mask4',
    'SD341': '_S0_USB_Default_Gateway1',
    'SD342': '_S0_USB_Default_Gateway2',
    'SD343': '_S0_USB_Default_Gateway3',
    'SD344': '_S0_USB_Default_Gateway4',
    'SD345': '_S0_USB_MAC_Address1',
    'SD346': '_S0_USB_MAC_Address2',
    'SD347': '_S0_USB_MAC_Address3',
    'SD348': '_S0_USB_MAC_Address4',
    'SD349': '_S0_USB_MAC_Address5',
    'SD350': '_S0_USB_MAC_Address6',
    'SD351': '_S0_Application_USAGE',
    'SD352': '_S0_Session_Cnt',
    'SD353': '_S0_DataUpdateCycleTime',
    'SD401': '_S1_ModuleId',
    'SD402': '_S1_Major_Version',
    'SD403': '_S1_Minor_Version',
    'SD404': '_S1_Hotfix_Version',
    'SD405': '_S1_Release_Version',
    'SD406': '_S1_CPU_USAGE',
    'SD407': '_S1_MEM_USAGE',
    'SD408': '_S1_ERROR_CODE',
    'SD409': '_S1_SD_TOTAL_MEM_L',
    'SD410': '_S1_SD_TOTAL_MEM_H',
    'SD411': '_S1_SD_FREE_MEM_L',
    'SD412': '_S1_SD_FREE_MEM_H',
    'SD413': '_S1_SD_USED_MEM_L',
    'SD414': '_S1_SD_USED_MEM_H',
    'SD415': '_S1_ETH_IP_Address1',
    'SD416': '_S1_ETH_IP_Address2',
    'SD417': '_S1_ETH_IP_Address3',
    'SD418': '_S1_ETH_IP_Address4',
    'SD419': '_S1_ETH_Subnet_Mask1',
    'SD420': '_S1_ETH_Subnet_Mask2',
    'SD421': '_S1_ETH_Subnet_Mask3',
    'SD422': '_S1_ETH_Subnet_Mask4',
    'SD423': '_S1_ETH_Default_Gateway1',
    'SD424': '_S1_ETH_Default_Gateway2',
    'SD425': '_S1_ETH_Default_Gateway3',
    'SD426': '_S1_ETH_Default_Gateway4',
    'SD427': '_S1_ETH_MAC_Address1',
    'SD428': '_S1_ETH_MAC_Address2',
    'SD429': '_S1_ETH_MAC_Address3',
    'SD430': '_S1_ETH_MAC_Address4',
    'SD431': '_S1_ETH_MAC_Address5',
    'SD432': '_S1_ETH_MAC_Address6',
    'SD433': '_S1_USB_IP_Address1',
    'SD434': '_S1_USB_IP_Address2',
    'SD435': '_S1_USB_IP_Address3',
    'SD436': '_S1_USB_IP_Address4',
    'SD437': '_S1_USB_Subnet_Mask1',
    'SD438': '_S1_USB_Subnet_Mask2',
    'SD439': '_S1_USB_Subnet_Mask3',
    'SD440': '_S1_USB_Subnet_Mask4',
    'SD441': '_S1_USB_Default_Gateway1',
    'SD442': '_S1_USB_Default_Gateway2',
    'SD443': '_S1_USB_Default_Gateway3',
    'SD444': '_S1_USB_Default_Gateway4',
    'SD445': '_S1_USB_MAC_Address1',
    'SD446': '_S1_USB_MAC_Address2',
    'SD447': '_S1_USB_MAC_Address3',
    'SD448': '_S1_USB_MAC_Address4',
    'SD449': '_S1_USB_MAC_Address5',
    'SD450': '_S1_USB_MAC_Address6',
    'SD451': '_S1_Application_USAGE',
    'SD452': '_S1_Session_Cnt',
    'SD453': '_S1_DataUpdateCycleTime'
}


def get_prefix(click_address : str) -> str :
    digits = 0
    for i, char in enumerate(click_address) :
        if not char.isalpha() : 
            digits = i
            break

    if digits < 1:
        raise ValueError(f"There is no letter prefix in '{click_address}'.")
    if digits > 3 :
        raise ValueError(f"You have a {digits}-letter prefix in '{click_address}' - the limit is 3.")
    return click_address[0:digits]

def addr_translate(click_address : str, use_true_address : bool = True) -> tuple[int, ModBusType, bool] :
    """Takes in an address for a Click Plus PLC register
    and returns information about it.

    Args:
        click_address (str): The address of the register in the Click Plus PLC
        use_true_address (bool): Returns the real address you have to use. ModBus is 1-addressed. It's very annoying.

    Returns:
        tuple(int, type, bool, optional[str]): Returns the ModBus address, the data type, and whether or not 
        you can write to it. It may also return a string at the end if there is a nickname for it.
    """

    # check to make sure the address is valid
    if len(click_address) < 2 : raise ValueError(f"`click_address` ({click_address}) must be at least length 2.")

    # dissect the address into the letters and numbers
    addr_prefix = get_prefix(click_address)
    addr_num = click_address[len(addr_prefix):]

    # check to make sure these are also valid
    EXCEPTIONS_TO_NUMERIC = ('XD0u', 'YD0u')
    if not addr_prefix.isalpha() : raise ValueError(f"`click_address` should begin with letters: {click_address}.")
    if not addr_num.isnumeric() and click_address not in EXCEPTIONS_TO_NUMERIC: 
        raise ValueError(f"`click_address` should have only numeric digits past the second character: {click_address}.")
    addr_num = int(addr_num) if click_address not in EXCEPTIONS_TO_NUMERIC else -1

    # snag the nickname if possible
    nickname = "" if click_address not in NICKNAMES else NICKNAMES[click_address]

    # adjust...

    # --- IGNORE ---
    # here's what this is doing. let's say we want to get C3's ModBus address.
    # addr_prefix would obviously be "C", and right now addr_num is 3.
    # later down the line, we're going to add some value to a base address to get the address we're looking for.
    # so, in C3's case, we're going to want to get 100003. the base address here is 100001, so we would only
    # want to add TWO. would it be easier to just adjust the base address? probably. and that is probably what i'm
    # going to do.
    # --- IGNORE ---

    # ModBus is 1-addressed. Annoying!
    if use_true_address : incrementor = addr_num - 1
    else : incrementor = addr_num

    # error string, in case i ever need to change it
    error_report = f"`click_address` with prefix {addr_prefix} out of range: {click_address}"

    match(addr_prefix) :
        case 'X' :
            ranges = [
                (1, 16, 100001),
                (21, 36, 100017),
                (101, 116, 100033),
                (201, 216, 100065),
                (301, 316, 100097),
                (401, 416, 100129),
                (501, 516, 100161),
                (601, 616, 100193),
                (701, 716, 100225),
                (801, 816, 100257)
            ]
            for start, end, base in ranges :
                if start <= addr_num <= end :
                    return (base + (incrementor - start)), ModBusType.Bit, False, nickname
            raise ValueError(error_report)
        
        case 'Y' :
            ranges = [
                (1, 16, 8193),
                (21, 36, 8209),
                (101, 116, 8225),
                (201, 216, 8257),
                (301, 316, 8289),
                (401, 416, 8321), 
                (501, 516, 8353),
                (601, 616, 8385),
                (701, 716, 8417),
                (801, 816, 8449)
            ]
            for start, end, base in ranges :
                if start <= addr_num <= end :
                    return (base + (incrementor - start)), ModBusType.Bit, True, nickname
            raise ValueError(error_report)
        
        case 'C' :
            if addr_num < 1 or addr_num > 2000 :
                raise ValueError(error_report)
            return (16385 + (incrementor - 1)), ModBusType.Bit, True, nickname
        
        case 'T' :
            if addr_num < 1 or addr_num > 500 :
                raise ValueError(error_report)
            return (145057 + (incrementor - 1)), ModBusType.Bit, False, nickname
        
        case 'CT' :
            if addr_num < 1 or addr_num > 250 :
                raise ValueError(error_report)
            return (149153 + (incrementor - 1)), ModBusType.Bit, False, nickname
        
        case 'SC' :
            ranges = [
                (1, 49, 161441),
                (50, 51, 61490),
                (52, 52, 161492),
                (53, 53, 61493),
                (54, 54, 161494),
                (55, 55, 61495),
                (56, 59, 161496),
                (60, 61, 61500),
                (62, 64, 161502),
                (65, 67, 61505),
                (68, 74, 161508),
                (75, 76, 61515),
                (77, 119, 161517),
                (120, 121, 61560),
                (122, 302, 161562),
                (303, 306, 61743),
                (307, 322, 161747),
                (323, 326, 61763),
                (327, 1000, 161767)
            ]
            writable = False
            for start, end, base in ranges :
                if start <= addr_num <= end :
                    return (base + (incrementor - start)), ModBusType.Bit, writable, nickname
                writable = not writable
            raise ValueError(error_report)
        
        case 'DS' :
            if addr_num < 1 or addr_num > 4500 :
                raise ValueError(error_report)
            return (400001 + (incrementor - 1)), ModBusType.Integer, True, nickname
        
        case 'DD' :
            if addr_num < 1 or addr_num > 1000 :
                raise ValueError(error_report)
            return (416385 + (incrementor - 1) * 2), ModBusType.Integer, True, nickname
        
        case 'DH' :
            if addr_num < 1 or addr_num > 500 :
                raise ValueError(error_report)
            return (424577 + (incrementor - 1)), ModBusType.Hexadecimal, True, nickname
        
        case 'DF' :
            if addr_num < 1 or addr_num > 500 :
                raise ValueError(error_report)
            return (428673 + (incrementor - 1) * 2), ModBusType.FloatingPoint, True, nickname
        
        case 'XD' :
            if addr_num < -1 or addr_num > 8 :
                raise ValueError(error_report)
            if addr_num == -1 : return 357346 - use_true_address, ModBusType.Hexadecimal, False, nickname # weird rule with XD0u
            if addr_num == 0 : return 357345 - use_true_address, ModBusType.Hexadecimal, False, nickname
            return (357347 + (incrementor - 1) * 2), ModBusType.Hexadecimal, False, nickname

        case 'YD' :
            if addr_num < -1 or addr_num > 8 :
                raise ValueError(error_report)
            if addr_num == -1 : return 457858 - use_true_address, ModBusType.Hexadecimal, True, nickname
            if addr_num == 0 : return 457857 - use_true_address, ModBusType.Hexadecimal, True, nickname
            return (457859 + (incrementor - 1) * 2), ModBusType.Hexadecimal, True, nickname
        
        case 'TD' :
            if addr_num < 1 or addr_num > 500 :
                raise ValueError(error_report)
            return (445057 + (incrementor - 1)), ModBusType.Integer, True, nickname
        
        case 'CTD' :
            if addr_num < 1 or addr_num > 250 :
                raise ValueError(error_report)
            return (449153 + (incrementor - 1) * 2), ModBusType.Integer2, True, nickname
        
        case 'SD' :
            switches = (
                29, 30, 31, 33, 34, 37, 40, 43, 50, 52, 60, 62, 106, 109, 112, 115, 140, 148,
                214, 216
            )
            # make sure data is valid
            if addr_num < 1 or addr_num > 1000 :
                raise ValueError(error_report)
            
            # run through the switches. leave once we're good.
            writable = False
            for switch in switches :
                if addr_num < switch : break
                writable = not writable

            # if we were allowed to write then leave
            if writable : 
                return (461441 + incrementor - 1), ModBusType.Integer, True, nickname
            else :
                return (361441 + incrementor - 1), ModBusType.Integer, False, nickname
        
        case 'TXT' :
            if addr_num < 1 or addr_num > 1000 :
                raise ValueError(error_report)
            # had to do it like this because it's weird. 
            # the problem was we were subtracting 1 if we wanted to use the true address up
            # at the top, but when we divide that number by 2 it gets off by a half. 
            # this fixes it (i'm pretty sure...)
            return int(436865 + (addr_num - 1) / 2) - use_true_address, ModBusType.Text, True, nickname
        
        case _ : 
            raise ValueError(f"Invalid prefix {addr_prefix}.")

def __test_addr_translate(use_lazy : bool) :
    """Tested the `addr_translate()` function based on the data extracted from the Click Plus PLC.
    """
    TEST_DEBUG = False
    with open('rawaddrdata.csv', 'r', newline='') as csvfile :
        csv_reader = csv.reader(csvfile)
        loop_broken = False
        for i, row in enumerate(csv_reader):

            # skip the first line
            if i == 0 : continue

            # print out the data we're about to use: row number, click address, and expected value.
            if TEST_DEBUG: print(f'\ntesting row {i + 1}')
            click_address = row[0]
            if TEST_DEBUG: print(f"{click_address=}")
            expected = int(row[2])
            if TEST_DEBUG: print(f"{expected=}")

            # the hex's have empty rows. they're not usable for tests. skip them.
            if click_address == "" : continue

            # try running the addr_translate function
            try :
                if use_lazy : result = __addr_translate_lazy(click_address)
                else : result, modbusType, writable, nickname = addr_translate(click_address, False)

            # if it errors, we want to know what line it failed on.
            except ValueError as e :
                print(e)
                print(i + 1)

            # if it didn't error, but the test still failed, let's report that.
            if result != expected :
                print(f"On line {i+1}, expected {expected} but got {result} for click address {click_address}.")
                loop_broken = True
                break
        if not loop_broken : print("All tests passed!")
        pass
    pass

def __addr_translate_lazy(click_address : str) :
    with open('rawaddrdata.csv', 'r', newline='') as csvfile :
        csv_reader = csv.reader(csvfile)
        for row in csv_reader :
            if row[0] == click_address :
                return int(row[2])

"""
print("test normal function")
start = time.time()
addr_translate("DH353")
end = time.time()
print(f"Total time taken: {end - start}")
print("\ntest pulling csv file")
start = time.time()
__addr_translate_lazy("DH353")
end = time.time()
print(f"Total time taken: {end - start}")
"""
def __get_nicknames_og() :
    """Retrieved the list of nicknames and their corresponding Click Plus addresses. Is now stored
    in a `dict` object called NICKNAMES.
    """
    with open('rawaddrdata.csv', 'r', newline='') as csvfile :
        csv_reader = csv.reader(csvfile)
        nicknames = []
        for row in csv_reader :
            if row[4] != "" :
                nicknames.append([row[0], row[4]])

        for n in nicknames :
            print(f"'{n[0]}': '{n[1]}',")

print(addr_translate("SD347", False))