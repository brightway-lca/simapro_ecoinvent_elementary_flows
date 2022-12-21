# Current status of the matching

CSV files with unmatched flows are in [`Mapping/Output/Unmatched`](https://github.com/brightway-lca/simapro_ecoinvent_elementary_flows/tree/main/Mapping/Output/Unmatched).

## ecoinvent flows

| Matched | Unmatched | Total |
| --- | --- | --- |
| {{ matched_ei_flows }} | {{ total_ei_flows - matched_ei_flows }} | {{ total_ei_flows }} |

## SimaPro flows

| Matched | Unmatched | Total |
| --- | --- | --- |
| {{ matched_sp_flows }} | {{ total_sp_flows - matched_sp_flows }} | {{ total_sp_flows }} |

## Unmatched ecoinvent flows by context

| Context | Unmatched | Total |
| --- | --- | --- |
{% for row in unmatched_ei_table %}| {{ row[0] }} | {{ row[1] }} | {{ row[2] }} |
{% endfor %}

## Unmatched SimaPro flows by context

| Context | Unmatched | Total |
| --- | --- | --- |
{% for row in unmatched_sp_table %}| {{ row[0] }} | {{ row[1] }} | {{ row[2] }} |
{% endfor %}
