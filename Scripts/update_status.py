from pathlib import Path
import pandas as pd

from jinja2 import Template 


BASE_DIR = Path(__file__).parent.parent.resolve()
MAPPED_FILE = BASE_DIR / "Mapping" / "Output" / "Mapped_files" / "SimaProv94-ecoinventEFv3.7.csv"
INPUTS_EI = BASE_DIR / "Mapping" / "Input" / "Flowlists" / "ecoinventEFv3.7.csv"
INPUTS_SP = BASE_DIR / "Mapping" / "Input" / "Flowlists" / "SimaProv9.4.csv"

    
def run():
    df_mapped = pd.read_csv(MAPPED_FILE)
    df_inputs_ei = pd.read_csv(INPUTS_EI)
    df_inputs_sp = pd.read_csv(INPUTS_SP)

    mask = ~df_inputs_sp['Flow UUID'].isin(set(df_mapped.SourceFlowUUID))
    df_unmatched_sp = df_inputs_sp[mask]
    sp_series = df_unmatched_sp.groupby("Context").size().sort_index()

    mask = ~df_inputs_ei['FlowUUID'].isin(set(df_mapped.TargetFlowUUID))
    df_unmatched_ei = df_inputs_ei[mask]
    ei_series = df_unmatched_ei.groupby("Context").size().sort_index()

    with open(BASE_DIR / "Templates" / 'status_template.md') as template_f:
        template = Template(template_f.read())
    output = template.render({
        "matched_ei_flows": len(set(df_mapped.TargetFlowUUID)),
        "total_ei_flows": len(set(df_inputs_ei['FlowUUID'])),
        "matched_sp_flows": len(set(df_mapped.SourceFlowUUID)),
        "total_sp_flows": len(set(df_inputs_sp['Flow UUID'])),
        "unmatched_ei_table": list(zip(ei_series.index, ei_series)),
        "unmatched_sp_table": list(zip(sp_series.index, sp_series)),
    })
    with open('status.md', "w+") as status_file:
        status_file.write(output)


if __name__ == "__main__":
    run()
