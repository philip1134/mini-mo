<%!
    import minimo.utils as flt
%>
${suite_name}

${summary}

% for case in counter.keys():
-------------------------------------------------
${case}: ${flt.format_duration(counter.get_duration_of(case))}
    % for flag in ("error", "exception", "warning"):
        <% lst = getattr(counter, "get_%s" % flag)(case) %>
${flag}: ${len(lst)}
        % for item in lst:
- ${item}
        % endfor
    % endfor

% endfor
