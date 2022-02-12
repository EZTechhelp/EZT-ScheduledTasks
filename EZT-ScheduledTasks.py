import os 
import sys 
ps_content=r'''
<#
    .Name
    EZT-ScheduledTasks

    .Version 
    0.1.0

    .SYNOPSIS
    Checks for scheduled tasks by name and enables or disables them

    .DESCRIPTION
       
    .Configurable Variables

    .Requirements
    - Powershell v3.0 or higher

    .EXAMPLE
    .\EZT-ScheduledTasks.ps1

    .OUTPUTS
    System.Management.Automation.PSObject

    .NOTES
    Author: EZTechhelp
    Site  : https://www.eztechhelp.com
#> 

#############################################################################
#region Configurable Script Parameters
#############################################################################

#---------------------------------------------- 
#region Function Select Variables
#----------------------------------------------
$Check_Task_Name = "''' + itsm.getParameter('Check_Task_Name') + '''"
$Task_MatchAny_Name = ([System.Convert]::ToBoolean(''' + itsm.getParameter('Task_MatchAny_Name') + ''')) #The matching name of the scheduled task to search for
$Task_StartsWith_Name = ([System.Convert]::ToBoolean(''' + itsm.getParameter('Task_StartsWith_Name') + '''))
$Task_Exact_Name = ([System.Convert]::ToBoolean(''' + itsm.getParameter('Task_Exact_Name') + ''')) #The exact name of the scheduled task to search for
$Enable_Task = ([System.Convert]::ToBoolean(''' + itsm.getParameter('Enable_Task') + ''')) #Enable (1) or Disables (0) all tasks matching provide name
#---------------------------------------------- 
#endregion Function Select Variables
#----------------------------------------------

#############################################################################
#endregion Configurable Script Parameters
#############################################################################

#############################################################################
#region Execution and Output - Functions or Code that executes required actions and/or performs output 
#############################################################################

#---------------------------------------------- 
#region Schedule Tasks
#----------------------------------------------
if($Task_MatchAny_Name){
  $Task_Name = "*$Check_Task_Name*"
  write-output "#### Checking for scheduled tasks matching name $Task_Name ####" 
  $scheduled_Task = (Get-scheduledtask -taskname "$Task_Name") | select * | where {$_.settings.Enabled -ne $Enable_Task}
}elseif($Task_StartsWith_Name){
  $Task_Name = "$Check_Task_Name*"
  write-output "#### Checking for scheduled tasks starting with name $Task_Name ####" 
  $scheduled_Task = (Get-scheduledtask -taskname "$Task_Name") | select * | where {$_.settings.Enabled -ne $Enable_Task}
}elseif($Task_Exact_Name){
  $Task_Name = $Check_Task_Name
  write-output "#### Checking for scheduled tasks with exact name $Task_Name ####" 
  $scheduled_Task = (Get-scheduledtask -taskname "$Task_Name") | select * | where {$_.settings.Enabled -ne $Enable_Task}
}else{
  write-warning "You must provide a task name to search for"
  exit
}


if($scheduled_Task){
  foreach($task in $scheduled_Task){
    write-output "`n>>>> Found Scheduled Tasks matching search criteria"
    write-output " | Task Name: $($task.taskname)"
    write-output " | Task State: $($task.State)"
    write-output " | Task Description: $($task.Description)"
    if($Enable_Task -and !$task.settings.Enabled){
      write-output ">>>> Enabling Task $($task.taskname)"
      $null = Enable-ScheduledTask -TaskName $task.taskname
    }elseif(!$Enable_Task -and $task.settings.Enabled){
      write-output ">>>> Disabling Task $($task.taskname)"
      $null = Disable-ScheduledTask -TaskName $task.taskname
    }else{
      write-output "No matching scheduled tasks were modified"
    } 
  }
}else{
  write-output "No Scheduled Tasks found matching name $Task_Name"
}

#---------------------------------------------- 
#endregion Schedule Tasks
#----------------------------------------------

#############################################################################
#endregion Execution and Output Functions
#############################################################################
'''

print ("iTarian RMM - Executing Powershell Script")

def ecmd(command):
    import ctypes
    from subprocess import PIPE, Popen
    
    class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)
    
    with disable_file_system_redirection():
        obj = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
    out, err = obj.communicate()
    ret=obj.returncode
    if ret==0:
        if out:
			return out.strip()
        else:
            return ret
    else:
        if err:
            return err.strip()
        else:
            return ret

file_name='EZT-ScheduledTasks.ps1'
file_path=os.path.join(os.environ['TEMP'], file_name)
with open(file_path, 'wb') as wr:
    wr.write(ps_content)

ecmd('powershell "Set-ExecutionPolicy Bypass"')
print ecmd('powershell "%s"'%file_path)

os.remove(file_path)