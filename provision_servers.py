import subprocess
import json
import os

def apply_terraform_with_variable(machines_to_run):
    """
    Apply Terraform configurations with the given machine names.

    :param machines_to_run: A list of machine names to be created.
    """
    # Convert the list to a JSON string
    machine_json = json.dumps(machines_to_run)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the Terraform command
    cmd = [
        'terraform', f'-chdir={script_dir}/terraform', 'apply', # specifies where config file is found
        '-auto-approve',  # Skip interactive approval; use cautiously!
        f'-var=machines_to_run={machine_json}',
        
    ]
    print(cmd)
    # Run the command and capture the output
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Check for errors and print the output
    if result.returncode != 0:
        print("Error running terraform:", result.stderr)
    else:
        print(result.stdout)

if __name__ == "__main__":
    # This creates all instances except Johannesburg and Sao Paolo
    # because they use different plans
    machines_to_run = {"ariatlanta":"atl", 
                       "ariamsterdam":"ams", 
                       "arichicago":"ord",
                       "aridallas": "dfw",
                       "arifrance": "fra",
                       "arilondon":"lhr",
                       "arimadrid":"mad",
                       "arimelbourne":"mel",
                       "arimexicocity": "mex",
                       "arimiami": "mia",
                       "arimumbai":"bom",
                       "aribangalore":"blr",
                       "ariparis":"cdg",
                       "ariseattle": "sea",
                       "ariseoul":"icn",
                       "arisiliconvalley":"sjc",
                       "arisingapore":"sgp",
                       "aristockholm":"sto",
                       "arisidney":"syd",
                       "aritokyo":"nrt",
                       "aritoronto":"yto",
                       "arila":"lax",
                       "ariwarsaw":"waw",
                       "arinj2":"ewr",
                       }
    apply_terraform_with_variable(machines_to_run)