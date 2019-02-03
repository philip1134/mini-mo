# -*- coding:utf-8 -*-
<%!
    import minimo.filters as flt
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
                color: #666; text-align: left; font-size: 13px; line-height: 18px;
                font-family: "Hiragino Sans GB","Hiragino Sans GB W3","Microsoft YaHei","微软雅黑",YouYuan,"幼圆",tahoma,arial,simsun,"宋体";
            }
            #header { position: relative; width: 100%; padding: 20px 0;  }
            h1 { font-size: 18px; }
            h2 { font-size: 16px; }
            .mmo-tip { font-size: 13px; font-weight: normal; color: #999; }
            .mmo-tip span { padding-right: 15px; }
            .mmo-em { color: #27ae60; padding: 0 5px; }
            .mmo-desktop { width: 100%; margin: 30px auto; text-align: center; }
            #foorter { text-align: center; }
        </style>
        </%text>
    </head>
    <body>
        <div id="header">
            <h1>${suite_name}</h1>
            <div class="mmo-tip">
                <span>
                    duration
                    <span class="mmo-em">${flt.format_duration(counter.get_duration_of_app()}</span>
                </span>
                % for flag in ("error", "exception", "warning", "success", "failure"):
                <span>
                    ${flag}
                    <span class="mmo-em">${getattr(counter, "total_%s" % flag)()}</span>
                </span>
                % endfor
            </div>
        </div>
        <div class="mmo-desktop">
        % for case in counter.keys():
            <div>
                <h2>{case}</h2>
                <div class="mmo-tip">
                    <span>
                        duration
                        <span class="mmo-em">${flt.format_duration(counter.get_duration_of(case))}</span>
                    </span>
                </div>
                <div>
                % for flag in ("error", "exception", "warning"):
                    <% lst = getattr(counter, "get_%s" % flag)(case) %>
                    <div>
                        ${flag}
                        <span class="mmo-em">${len(lst)}</span>
                    </div>
                    % for item in lst:
                        <div>${item}</div>
                    % endfor
                % endfor
                </div>
            </div>
        % endfor
        </div>
        <div id="footer">printed by mini-mo</div>
    </body>
</html>