## Installation and Configuration

**EZT-ScheduledTasks.ps1** 

- Powershell only version, main script

**EZT-ScheduledTasks.py**

- Python only version that is also the source code for the iTarian Procedure

**EZT-ScheduledTasks.json**

- The Python version exported from iTarian. Use this to quickly import into your iTarian procedures

### Installation for iTarian Procedures

1. **Download the ITSM procedure** 
2. Within your ITSM portal, import the procedure under **Configuration Templates - Procedures**
3. Configure desired **procedure name, alert settings**..etc
4. Configure the **default parameters** for the procedure from the **Parameters tab** of the script. See **Configuration Parameters** below for explanations of each parameter
5. Click **Save - Ready to Review - Approve** to finish. **Assign to a profile** and optionally a schedule of your liking
6. **(Recommended)** Run the new procedure on a single **test machine** to ensure its working or configured as expected

#### iTarian Configuration

- This script can be configured by editing the **parameter options** within the iTarian RMM procedure 

#### Powershell Configuration

- If you wish to use the pure Powershell shell script version, use the configuration variables located in the region **Configurable Script Parameters** located near the top of the script 

### Configuration Parameters/Variables

Only enable 1 of the task searching options (matchany, startswith,exact) If multiple enabled, only the first option is honored

_**Note: 1 = Enabled, 0 = Disabled**_

-  **Check_Task_Name**
   - Default: Google
   - Name of the Scheduled Task to check for 
   
-  **Task_MatchAny_Name**
   - Default: 0
   - Find any tasks matching name

-  **Task_StartsWith_Name**
   - Default: 1
   - Find tasks starting with name

-  **Task_Exact_Name**
   - Default: 0
   - Find tasks with exact name

-  **Enable_Task**
   - Default: 0
   - Enables or Disables tasks found
