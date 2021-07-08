import subprocess


## Requirements: wsman (apt install wsmancli)

## https://www.dmtf.org/sites/default/files/standards/documents/DSP1027_2.0.0.pdf

## Functioning of this script probably depends on the specific AMT hardware (implemented cim schema)

power_down_command = '<p:RequestPowerStateChange_INPUT xmlns:p="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_PowerManagementService"> \
               <p:PowerState>8</p:PowerState> \
               <p:ManagedElement xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:wsman="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd"> \
               <wsa:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</wsa:Address> \
               <wsa:ReferenceParameters><wsman:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ComputerSystem</wsman:ResourceURI> \
               <wsman:SelectorSet><wsman:Selector Name="CreationClassName">CIM_ComputerSystem</wsman:Selector> \
               <wsman:Selector Name="Name">ManagedSystem</wsman:Selector> \
               </wsman:SelectorSet></wsa:ReferenceParameters></p:ManagedElement></p:RequestPowerStateChange_INPUT>'


power_up_command = '<p:RequestPowerStateChange_INPUT xmlns:p="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_PowerManagementService"> \
               <p:PowerState>2</p:PowerState> \
               <p:ManagedElement xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:wsman="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd"> \
               <wsa:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</wsa:Address> \
               <wsa:ReferenceParameters><wsman:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ComputerSystem</wsman:ResourceURI> \
               <wsman:SelectorSet><wsman:Selector Name="CreationClassName">CIM_ComputerSystem</wsman:Selector> \
               <wsman:Selector Name="Name">ManagedSystem</wsman:Selector> \
               </wsman:SelectorSet></wsa:ReferenceParameters></p:ManagedElement></p:RequestPowerStateChange_INPUT>'


power_hard_reset_command = '<p:RequestPowerStateChange_INPUT xmlns:p="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_PowerManagementService"> \
               <p:PowerState>10</p:PowerState> \
               <p:ManagedElement xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:wsman="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd"> \
               <wsa:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</wsa:Address> \
               <wsa:ReferenceParameters><wsman:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_ComputerSystem</wsman:ResourceURI> \
               <wsman:SelectorSet><wsman:Selector Name="CreationClassName">CIM_ComputerSystem</wsman:Selector> \
               <wsman:Selector Name="Name">ManagedSystem</wsman:Selector> \
               </wsman:SelectorSet></wsa:ReferenceParameters></p:ManagedElement></p:RequestPowerStateChange_INPUT>'


force_pxe_boot_command =   '<p:ChangeBootOrder_INPUT xmlns:p="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootConfigSetting"> \
                           <p:Source xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:wsman="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd"> \
                           <wsa:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</wsa:Address> \
                           <wsa:ReferenceParameters><wsman:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</wsman:ResourceURI> \
                           <wsman:SelectorSet><wsman:Selector wsman:Name="InstanceID">Intel(r) AMT: Force PXE Boot</wsman:Selector></wsman:SelectorSet> \
                           </wsa:ReferenceParameters></p:Source></p:ChangeBootOrder_INPUT>'


force_local_disk_command = '<p:ChangeBootOrder_INPUT xmlns:p="http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootConfigSetting"> \
                            <p:Source xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:wsman="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd"> \
                            <wsa:Address>http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</wsa:Address> \
                            <wsa:ReferenceParameters><wsman:ResourceURI>http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootSourceSetting</wsman:ResourceURI> \
                            <wsman:SelectorSet><wsman:Selector wsman:Name="InstanceID">Intel(r) AMT: Force Hard-drive Boot</wsman:Selector></wsman:SelectorSet> \
                            </wsa:ReferenceParameters></p:Source></p:ChangeBootOrder_INPUT>'


wsman_boot_device_method = ''' 'ChangeBootOrder' 'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_BootConfigSetting?InstanceID="Intel(r) AMT: Boot Configuration 0"' '''


wsman_power_method = ''' 'RequestPowerStateChange' 'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_PowerManagementService?SystemCreationClassName="CIM_ComputerSystem"&SystemName="Intel(r) AMT"&CreationClassName="CIM_PowerManagementService"&Name="Intel(r) AMT Power Management Service"' '''



def get_power_state(targetip:str = "", port:str = "16992", password:str = "", username:str = "admin"):
    if(targetip == ""):
        print("You need to provide the parameter targetip!")
        return

    if(password == ""):
        print("You need to provide the parameter password!")
        return

    command = "wsman --port " + port + " --hostname " + targetip + " --username " + username + " --password " + password + " --noverifypeer --noverifyhost --optimize --encoding utf-8 enumerate 'http://schemas.dmtf.org/wbem/wscim/1/cim-schema/2/CIM_AssociatedPowerManagementService'"
    print(command)
    subprocess.call(command , shell=True)
    # Look for that line: <h:PowerState>X</h:PowerState>
    return

def hard_reset(targetip:str = "", port:str = "16992", password:str = "", username:str = "admin"):
    if(targetip == ""):
        print("You need to provide the parameter targetip!")
        return

    if(password == ""):
        print("You need to provide the parameter password!")
        return

    command = "wsman --port " + port + " --hostname " + targetip + " --username " + username + " --password " + password + " --noverifypeer --noverifyhost --input - invoke --method "
    command = command + wsman_power_method
    command = "echo '" + power_hard_reset_command + "' | " + command
    print(command)
    subprocess.call(command , shell=True)
    return


def power_down(targetip:str = "", port:str = "16992", password:str = "", username:str = "admin"):
    if(targetip == ""):
        print("You need to provide the parameter targetip!")
        return

    if(password == ""):
        print("You need to provide the parameter password!")
        return

    command = "wsman --port " + port + " --hostname " + targetip + " --username " + username + " --password " + password + " --noverifypeer --noverifyhost --input - invoke --method "
    command = command + wsman_power_method
    command = "echo '" + power_down_command + "' | " + command
    print(command)
    subprocess.call(command , shell=True)
    return

def power_up(targetip:str = "", port:str = "16992", password:str = "", username:str = "admin"):
    if(targetip == ""):
        print("You need to provide the parameter targetip!")
        return
    
    if(password == ""):
        print("You need to provide the parameter password!")
        return

    command = "wsman --port " + port + " --hostname " + targetip + " --username " + username + " --password " + password + " --noverifypeer --noverifyhost --input - invoke --method "
    command = command + wsman_power_method
    command = "echo '" + power_up_command + "' | " + command
    print(command)
    subprocess.call(command , shell=True)
    return

def set_boot_from_disk(targetip:str = "", port:str = "16992", password:str = "", username:str = "admin"):
    if(targetip == ""):
        print("You need to provide the parameter targetip!")
        return
    
    if(password == ""):
        print("You need to provide the parameter password!")
        return

    command = "wsman --port " + port + " --hostname " + targetip + " --username " + username + " --password " + password + " --noverifypeer --noverifyhost --input - invoke --method "
    command = command + wsman_boot_device_method
    command = "echo '" + force_local_disk_command + "' | " + command
    print(command)
    subprocess.call(command , shell=True)
    return
    
def set_boot_from_network(targetip:str = "", port:str = "16992", password:str = "", username:str = "admin"):
    if(targetip == ""):
        print("You need to provide the parameter targetip!")
        return

    if(password == ""):
        print("You need to provide the parameter password!")
        return

    command = "wsman --port " + port + " --hostname " + targetip + " --username " + username + " --password " + password + " --noverifypeer --noverifyhost --input - invoke --method "
    command = command + wsman_boot_device_method
    command = "echo '" + force_pxe_boot_command + "' | " + command
    print(command)
    subprocess.call(command , shell=True)
    return

