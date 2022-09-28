""" A script to update the counts of matches. """
import pandas as pd
import os

from jinja2 import Template 


MAPPED_FILE = "Mapping/Output/Mapped_files/SimaProv94-ecoinventEFv3.7.csv"
INPUTS_EI = "Mapping/Input/Flowlists/ecoinventEFv3.7.csv"
INPUTS_SP = "Mapping/Input/Flowlists/SimaProv9.4.csv"
STATUS_DEBUG = os.getenv('STATUS_DEBUG', True) 
DRY_RUN = os.getenv("DRY_RUN", False)
def update_status_file(new_status:dict):
    """Load the status_update template and update the status file `status.md`.

    Args:
        new_status (dict): keys: 
            total_sp_flows, 
            total_ei_flows,
            matched_flows

    """
    with open('status_template.md') as template_f:
        template = Template(template_f.read())
    output = template.render(new_status)
    if DRY_RUN:
        print("Not updating the file, only dry run")
        print(f"This would be output: {output}")
    else:
        with open('status.md', "w+") as status_file:
            status_file.write(output)



def load_data():
    """Extract the data from the csv files.

    Returns:
        def_mapped, def_inputs_ei, df_inputs_sp 3 dataframes, one for mappings, one for ecoinvent inputs one for simapro inputs
        

    """
    df_mapped = pd.read_csv(MAPPED_FILE)
    df_inputs_ei = pd.read_csv(INPUTS_EI)
    df_inputs_sp = pd.read_csv(INPUTS_SP)

    return df_mapped, df_inputs_ei, df_inputs_sp

    
def run():
    df_mapped, df_inputs_ei, df_inputs_sp = load_data()

    if STATUS_DEBUG:
        print(df_mapped.info())
        print(df_inputs_ei.info())
        print(df_inputs_sp.info())

    matched_mask = pd.Series(df_inputs_ei['FlowUUID']).isin(df_mapped['TargetFlowUUID'])

    ei_matched_to_sp_sum = sum(matched_mask)

    missing_ei_df = pd.DataFrame(df_inputs_ei[~ matched_mask])


    update_status_file({
        'total_sp_flows':len(df_inputs_sp), 
        'total_ei_flows':len(df_inputs_ei),
        'total_matched_flows':len(df_mapped),
        'ei_matched_to_sp_sum':ei_matched_to_sp_sum,
        'missing_ei_table': missing_ei_df.to_markdown(index=False),
        })

if __name__ == "__main__":
    run()
