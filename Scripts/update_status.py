from pathlib import Path
import pandas as pd

from jinja2 import Template 


BASE_DIR = Path(__file__).parent.parent.resolve()
MAPPED_FILE = BASE_DIR / "Mapping" / "Output" / "Mapped_files" / "SimaProv94-ecoinventEFv3.7.csv"
INPUTS_EI = BASE_DIR / "Mapping" / "Input" / "Flowlists" / "ecoinventEFv3.7.csv"
INPUTS_SP = BASE_DIR / "Mapping" / "Input" / "Flowlists" / "SimaProv9.4.csv"

UNMATCHED_DIR = BASE_DIR / "Mapping" / "Output" / "Unmatched"
UNMATCHED_DIR.mkdir(exist_ok=True)
BY_CATEGORY = UNMATCHED_DIR / "By category"
BY_CATEGORY.mkdir(exist_ok=True)

def run():
    df_mapped = pd.read_csv(MAPPED_FILE)
    df_inputs_ei = pd.read_csv(INPUTS_EI)
    df_inputs_sp = pd.read_csv(INPUTS_SP)

    mask = ~df_inputs_sp['Flow UUID'].isin(set(df_mapped.SourceFlowUUID))
    df_unmatched_sp = df_inputs_sp[mask]
    sp_series = df_unmatched_sp.groupby("Context").size().sort_index()
    sp_series_all = df_inputs_sp.groupby("Context").size()

    mask = ~df_inputs_ei['FlowUUID'].isin(set(df_mapped.TargetFlowUUID))
    df_unmatched_ei = df_inputs_ei[mask]
    ei_series = df_unmatched_ei.groupby("Context").size().sort_index()
    ei_series_all = df_inputs_ei.groupby("Context").size()

    df_unmatched_sp.to_csv(UNMATCHED_DIR / "SimaProv9.4.csv", index=False)
    df_unmatched_ei.to_csv(UNMATCHED_DIR / "ecoinventEFv3.7.csv", index=False)

    for label in df_unmatched_sp.groupby("Context").size().index:
        filtered_dp = df_unmatched_sp[df_unmatched_sp.Context == label]
        filtered_dp.to_csv(BY_CATEGORY / "SimaProv9.4 - {}.csv".format(label.replace("/", "-")), index=False)

    for label in df_unmatched_ei.groupby("Context").size().index:
        filtered_dp = df_unmatched_ei[df_unmatched_ei.Context == label]
        filtered_dp.to_csv(BY_CATEGORY / "ecoinventEFv3.7 - {}.csv".format(label.replace("/", "-")), index=False)

    with open(BASE_DIR / "Templates" / 'status_template.md') as template_f:
        template = Template(template_f.read())
    output = template.render({
        "matched_ei_flows": len(set(df_mapped.TargetFlowUUID)),
        "total_ei_flows": len(set(df_inputs_ei['FlowUUID'])),
        "matched_sp_flows": len(set(df_mapped.SourceFlowUUID)),
        "total_sp_flows": len(set(df_inputs_sp['Flow UUID'])),
        "unmatched_ei_table": [(label, ei_series.at[label], ei_series_all.at[label]) for label in ei_series.index],
        "unmatched_sp_table": [(label, sp_series.at[label], sp_series_all.at[label]) for label in sp_series.index],
    })
    with open('status.md', "w+") as status_file:
        status_file.write(output)


if __name__ == "__main__":
    run()
