��    %      D  5   l      @     A     `     {     �     �  &   �     �          !     1     B     U     d     w  	   �     �     �     �     �     �     �     �     
          1     H     ^     z     �  $   �     �  )   �  +     (   ?     h  %   �  X  �  4     E   6  H   |  >   �  J   	  9   O	  <   �	  ?   �	  (   
     /
     O
     c
  
   q
  =  |
  -   �  *  �       9   $     ^     o  (   �     �     �     �     �  �   �     �     �  a   �     (     =  D   Q  D   �  >   �  H     P   c                               	           "                                $                %                    !   
                             #                                     error.action_exception_occured error.author_name_required error.case_author_name_required error.exception_in_case error.fail_to_create_file error.invalid_minimo_project_directory error.unrecognized_command error.wrong_usage format.time.day format.time.hour format.time.minute format.time.ms format.time.second help.app help.init help.new info.add_task info.case_created info.create_dir info.create_file info.creating_case_by_template info.creating_case_dir info.executing_task info.failed_action info.not_standard_case info.performer_report info.prepare_to_create_case info.report_case_exception info.report_mission_complete info.skip_creating_dir_for_existence info.start_action warning.abort_creating_case_for_existence warning.abort_creating_case_for_no_template warning.abort_creating_dir_for_existence warning.not_standard_case warning.unrecognized_project_template Project-Id-Version: mini-mo 0.1.0
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-02-23 11:14+0800
PO-Revision-Date: 2018-02-23 11:14+0800
Last-Translator: philip1134 <philip1134@imior.com>
Language-Team: philip1134 <philip1134@imior.com>
Language: zh-cn
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
 执行时产生异常，请检查任务代码！
{0} 请指定用例作者名： minimo new TASK-SUITE/TASK-CASE -a AUTHOR 必须为任务用例指定作者名: minimo new [task-case] -a [author] 执行 {0} 时产生异常，请检查任务用例的代码！ 创建文件 {0} 失败，请重新创建这个文件！
失败原因:
{1} 非minimo项目，请使用 'minimo help' 查看帮助。 未识别的命令，请使用 'minimo help' 查看帮助。 错误的使用方法，请使用 'minimo help' 查看帮助。 {:d} 天 {:d} 小时 {:d} 分 {:.3f} 秒 {:d} 小时 {:d} 分 {:.3f} 秒 {:d} 分 {:.3f} 秒 {:.3f} 毫秒 {:.3f} 秒 {project_name} 功能执行者。以cli形式将 {project_name} 功能封装，包括生成任务用例代码模板，运行用例等。

用法： minimo <sub-command> [options] [args]

可用的子命令：
new    - 创建项目
case   - 创建任务用例
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

- help: 显示帮助信息 创建项目
用法: minimo init PROJECT_NAME 创建任务用例
用法: minimo new TASK_SUITE/TASK_CASE -a AUTHOR
或:   minimo new TASK_CASE -a AUTHOR

将根据项目的用例模板初始化用例代码，代码将被创建在
	project.root/cases/TASK_SUITE/TASK_CASE
如果TASK_SUITE目录下有用例模板，则优先根据该模板创建 添加任务 {0} 任务用例创建完成，请查看目录 {0}.root/cases 创建目录 {0} 	创建文件 {0} 使用项目模板创建任务用例 {0} 创建目录 cases/{0} 执行任务 {0} 异常操作: {0}
{1} 非标准用例  
{split}
任务结束
{success} 个成功
{failure} 个失败
{error} 个错误
{warning} 个警告
{exception} 个异常

共使用了 {duration}
{split} 准备创建任务用例... {0}: 执行异常
{1}  

{0}
任务结束
共有 {1} 个任务被执行， 其中 {2} 个任务在执行时产生异常 目录 {0} 已存在 执行操作 {0}... 目录 cases/{0} 已存在，放弃在此目录下的创建操作！ 没有找到任务模板，放弃在 cases/{0} 下的创建操作！ 目录 {0} 已存在，放弃在此目录下的创建操作！ {0} 不是 {1} 的标准任务用例，请检查路径或单独执行！ 未识别的模板名 '{0}'，将使用 minimo 提供的默认模板创建项目 