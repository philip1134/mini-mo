��          �   %   �      0     1     Q     i     �     �     �     �     �     �     �     �          0     D     [     q     �     �  $   �  )   �  +     (   @     i  X  �  A   �  &     $   E  A   j  8   �  '  �       6        Q     f  #   w     �     �     �  �   �     j     �  V   �     �  3     6   H  -     9   �         
                                                          	                                                            error.case_author_name_required error.exception_in_case error.fail_to_create_file error.unrecognized_command error.wrong_usage help.app info.add_task info.case_created info.create_dir info.create_file info.creating_case_by_template info.creating_case_dir info.executing_task info.not_standard_case info.performer_report info.prepare_to_create_case info.report_case_exception info.report_mission_complete info.skip_creating_dir_for_existence warning.abort_creating_case_for_existence warning.abort_creating_case_for_no_template warning.abort_creating_dir_for_existence warning.not_standard_case Project-Id-Version: mini-mo 0.1.0
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-02-23 11:14+0800
PO-Revision-Date: 2018-02-23 11:14+0800
Last-Translator: philip1134 <philip1134@imior.com>
Language-Team: philip1134 <philip1134@imior.com>
Language: en-us
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
 case author name required: python {0} new [task-case] -a [author] exception occured while performing {0} fail to create file {0}!
reason:
{1} unrecognized command, please check out help info by 'minimo help' wrong usage, please check out help info by 'minimo help' {project_name} 功能执行者。以cli形式将 {project_name} 功能封装，包括生成任务用例代码模板，运行用例等。

用法： minimo <sub-command> [options] [args]

可用的子命令：
new    - 创建任务用例
run    - 执行指定的任务用例
help   - 显示帮助信息

子命令详解：
- new: 创建任务用例
用法: minimo new [test-case] -a [author]

[test-case] 格式为 '项目名称/任务用例名称'，例如: 'my_testsuite/my_first_test_case'。意即 my_testsuite 项目下的任务用例 my_first_test_case

[author] 为作者名，建议使用姓名拼音。同一人在项目中请保持同一名称。

- run: 执行指定的任务用例 (python)
用法: minimo run [test-case]

[test-case] 格式为 '项目名称' 或者 '项目名称/任务用例名称'，例如: 'my_testsuite' 或 'my_testsuite/my_first_test_case'，如果只指定项目名称，则执行该项目下的所有任务用例。如果指定项目名称和任务用例名称，则只执行指定的任务用例。

- help: 显示帮助信息 add task {0} case created, please check it out under {0}.root/cases create directory {0} 	create file {0} create case by project template {0} create directory cases/{0} run task {0} not standard case {split}
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
totally {1} cases were executed,  {2} cases raised exception. directory {0} already exsited directory cases/{0} already existed, skip creating! no template found, abort creating task under cases/{0} directory {0} already existed, skip creating! {0} is not {1} standard case, please run it respectively. 