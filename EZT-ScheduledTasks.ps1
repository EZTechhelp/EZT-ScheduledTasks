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
$Check_Task_Name = 'Google' #The name of the scheduled task to search for
$Task_MatchAny_Name = ([System.Convert]::ToBoolean(0)) #Find any tasks matching name
$Task_StartsWith_Name = ([System.Convert]::ToBoolean(1)) #Find tasks starting with name
$Task_Exact_Name = ([System.Convert]::ToBoolean(0)) #Find tasks with exact name
$Enable_Task = ([System.Convert]::ToBoolean(0)) #Enable (1) or Disables (0) all tasks matching provide name
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