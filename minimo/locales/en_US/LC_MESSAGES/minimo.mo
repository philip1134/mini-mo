��    '      T  5   �      `     a     �     �     �     �  &   �       #   /     S     e     u     �     �     �     �  	   �  	   �     �     �     �     �     
          +     J     a     u     �     �     �     �     �  $   	     .  )   @  +   j  (   �     �  X  �  3   2  ?   f  A   �  &   �  $   	  D   4	  6   y	  $   �	  -   �	  &   
     *
     H
  	   \
  
   f
  i   q
     �
  :  �
  �  ,  u  �     .  6   ;     r     �  #   �     �     �     �     �  �        �     �  V   �     0     N  3   b  6   �  -   �  9   �                              
   #       %   "                                                          '       $      	             !            &                                      error.action_exception_occured error.author_name_required error.case_author_name_required error.exception_in_case error.fail_to_create_file error.invalid_minimo_project_directory error.unrecognized_command error.unrecognized_project_template error.wrong_usage format.time.day format.time.hour format.time.minute format.time.ms format.time.second help.app help.help help.init help.new help.run info.add_task info.case_created info.create_dir info.create_file info.creating_case_by_template info.creating_case_dir info.executing_task info.failed_action info.not_standard_case info.performer_report info.prepare_to_create_case info.report_case_exception info.report_mission_complete info.skip_creating_dir_for_existence info.start_action warning.abort_creating_case_for_existence warning.abort_creating_case_for_no_template warning.abort_creating_dir_for_existence warning.not_standard_case Project-Id-Version: mini-mo 0.1.0
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-02-23 11:14+0800
PO-Revision-Date: 2018-02-23 11:14+0800
Last-Translator: philip1134 <philip1134@imior.com>
Language-Team: philip1134 <philip1134@imior.com>
Language: en-us
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
 error occured, please check out your task code!
{0} author name required: minimo new TASK-SUITE/TASK-CASE -a AUTHOR case author name required: python {0} new [task-case] -a [author] exception occured while performing {0} fail to create file {0}!
reason:
{1} not in minimo project root folder，please get help by 'minimo help' unrecognized command, please get help by 'minimo help' unrecognized project template '{0}'. wrong usage, please get help by 'minimo help' {:d} day {:d} hour {:d} min {:.3f} sec {:d} hour {:d} min {:.3f} sec {:d} min {:.3f} sec {:.3f} ms {:.3f} sec ** {project_name} **

usage: minimo <sub-command> [options] [args]

available sub commands
{sub_commands} show help information create a new minimo project
usage: minimo init PROJECT_NAME -t TEMPLATE_NAME
-t TEMPLATE_NAME 指定使用的项目模板，选填。
如果 TEMPLATE_NAME 为模板名称，则会在 minimo 的模板目录查找对应的项目模板；
如果为目录地址，则根据该地址提供的项目模板创建项目。 create a new task case by the template
用法: minimo new TASK_SUITE/TASK_CASE -a AUTHOR
或:   minimo new TASK_CASE -a AUTHOR

根据项目用例模板初始化用例代码，代码被创建在
	project.root/cases/TASK_SUITE/TASK_CASE
如果TASK_SUITE目录下有用例模板，则优先使用该模板创建
-a AUTHOR 指定作者名，必填。同一人在项目中建议保持同一名称。 执行指定的任务用例集或用例
用法: minimo run [task-suite]
或: minimo run [task-suite/task-case]

即指定的task格式为 '用例集' 或者 '用例集/用例名称'
例如: 'my_tasksuite' 或 'my_tasksuite/my_taskcase'，如果指定任务集名称，则执行该项目下的所有任务用例。如果指定用例名称，则执行指定的任务用例。 add task {0} case created, please check it out under {0}.root/cases create directory {0} 	create file {0} create case by project template {0} create directory cases/{0} run task {0} failed action: {0}
{1} not standard case  
{split}
mission complete!
{success} success
{failure} failure
{error} error
{warning} warning
{exception} exception

totally cost {duration}
{split} prepare to create case... {0}: exception occured
{1}  

{0}
mission complete!
totally {1} cases were executed,  {2} cases raised exception. directory {0} already exsited start action {0}... directory cases/{0} already existed, skip creating! no template found, abort creating task under cases/{0} directory {0} already existed, skip creating! {0} is not {1} standard case, please run it respectively. 