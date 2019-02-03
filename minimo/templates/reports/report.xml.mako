<report>
    <suite>
        <name>
            ${suite_name}
        </name>
        <duration>
            ${counter.get_duration_of_app()}
        </duration>
        <details>
        % for flag in ("error", "exception", "warning", "success", "failure"):
            <${flag}>
                <count>
                    ${getattr(counter, "total_%s" % flag)()}
                </count>
            </${flag}>
        % endfor
        </details>
    </suite>
    <cases>
    % for case in counter.keys():
        <case>
            <name>
                ${case}
            </name>
            <duration>
                ${counter.get_duration_of(case)}
            </duration>
            <details>
            % for flag in ("error", "exception", "warning"):
                <% lst = getattr(counter, "get_%s" % flag)(case) %>
                <${flag}>
                    <count>
                        ${len(lst)}
                    </count>
                    <items>
                    % for item in lst:
                        <item>
                            ${item}
                        </item>
                    % endfor
                    </items>
                </${flag}>
            % endfor
            </details>
        </case>
    % endfor
    </cases>
</report>