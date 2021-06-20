# -*- coding:utf-8 -*-
<%!
    import minimo.utils as flt
%>
<!DOCTYPE HTML>
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>${suite_name}</title>
        <%text>
        <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
        <style type="text/css">
            body {
                margin: 0; padding: 0; outline: none; background: #fff;
                color: #666; text-align: left; font-size: 13px; line-height: 20px;
                font-family: "Hiragino Sans GB","Hiragino Sans GB W3","Microsoft YaHei","微软雅黑",YouYuan,"幼圆",tahoma,arial,simsun,"宋体";
            }
            a { text-decoration: none; color: #2980b9; }
            .clearfix:before, .clearfix:after { content: " "; display: table; }
            .clearfix:after { clear: both; }
            .wrapper { position: relative; margin: 30px; }
            #header { position: relative; width: 100%; }
            .mmo-bar { position: absolute; left: 0; top: 1px; bottom: 1px; width: 4px; background-color: #3498db; }
            .mmo-tip { font-size: 13px; font-weight: normal; color: #999; padding: 0 0 10px 0; }
            .mmo-tip span { padding-right: 10px; }
            .mmo-em { color: #27ae60; padding: 0 5px; }
            .mmo-desktop { width: 100%; margin: 30px auto; }
            .mmo-section { margin-bottom: 30px; }
            .mmo-block { margin-bottom: 10px; }
            .mmo-item { position: relative; padding: 0 0 0 15px; margin: 5px 0 5px 10px; }
            .mmo-flag { float: left; padding: 0 5px; background: #eee; }
            .mmo-radius { -webkit-border-radius: 3px; -khtml-border-radius: 3px; -moz-border-radius: 3px; border-radius: 3px; }
            #footer { position: fixed; left: 0; bottom: 0; right: 0; padding: 10px 0; text-align: center; }
        </style>
        </%text>
    </head>
    <body>
        <div class="wrapper">
            <div id="header">
                <h1>${suite_name}</h1>
                <div class="mmo-tip">
                    <span>
                        duration:
                        <span class="mmo-em">
                            ${flt.format_duration(counter.get_duration_of_app())}
                        </span>
                    </span>
                    % for flag in ("error", "exception", "warning", "success", "failure"):
                    <span>
                        ${flag}:
                        <span class="mmo-em">
                            ${getattr(counter, "total_%s" % flag)()}
                        </span>
                    </span>
                    % endfor
                </div>
            </div>
            <div class="mmo-desktop">
            % for case in counter.keys():
                <div class="mmo-section">
                    <h2>${case}</h2>
                    <div class="mmo-tip">
                        <span>
                            duration:
                            <span class="mmo-em">
                                ${flt.format_duration(counter.get_duration_of(case))}
                            </span>
                        </span>
                    </div>
                    <div>
                    % for flag in ("error", "exception", "warning"):
                        <% lst = getattr(counter, "get_%s" % flag)(case) %>
                        <div class="mmo-block">
                            <div class="clearfix">
                                <div class="mmo-flag mmo-radius">
                                    ${flag}:
                                    <span class="mmo-em">${len(lst)}</span>
                                </div>
                            </div>
                            % for item in lst:
                                <div class="mmo-item">
                                    <div class="mmo-bar mmo-radius"></div>
                                    ${item}
                                </div>
                            % endfor
                        </div>
                    % endfor
                    </div>
                </div>
            % endfor
            </div>
            <div id="footer">
                <a href="https://github.com/philip1134/mini-mo" target="_blank">printed by mini-mo</a>
            </div>
        </div>
    </body>
</html>