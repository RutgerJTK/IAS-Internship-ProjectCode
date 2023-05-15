from flask import Flask, render_template, request
import marigold_boot_req

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('index.html', species_dict=gen_spec_info_dict, RA_info_dict=RA_dict, MA_supply_dict=supply_table_html )


@app.route('/species/<species_name>')
def species_page(species_name):
    selected_species = request.args.get('selected_species')
    species_info = gen_spec_info_dict.get(species_name)
    species_risk_info = RA_dict.get(names_dict[species_name])
    RA_site_list = []
    href_list = []
    risk_starts = [" 'Features factsheet on Nobanis", " 'Datasheet by CABI:", " 'CABI", " 'FWS",
                    " 'Has RA on NNSS Great Britain:", " 'Assessed (to some degree) on Glansis:", " 'Assessed (to some degree) on INPN", 
                    " 'Registered on BDI:"," 'Species EICAT classification:"]
    print(species_risk_info)
    last = [-2, -1]
    
    species_risk_info = species_risk_info[1:]
    print(species_name)
    for i in range(len(species_risk_info)):
        if species_risk_info[i] == species_risk_info[-1]:
            last = [-3, -2]
        if "On Michigan's watchlist" in species_risk_info[i]:
            species_risk_info[i] = species_risk_info[i][3:last[0]]
            print("heui")
        if " 'ISNA - no RA:" in species_risk_info[i]:
            species_risk_info[i] = species_risk_info[i][2:last[0]]
        if " 'ISNA - has RA:" in species_risk_info[i]:
            species_risk_info[i] = species_risk_info[i][2:last[0]]
        if " 'Species general info available on:" in species_risk_info[i]:
            species_risk_info[i] = species_risk_info[i][2:last[0]]
        for j in range(len(risk_starts)):         
            if species_risk_info[i].startswith(risk_starts[j]):
                species_risk_info[i] = species_risk_info[i][2:last[1]]

    RA_site_list, href_list = [item.split(": ")[0] for item in species_risk_info], [item.split(": ")[1] for item in species_risk_info]
    print(RA_site_list, href_list)
    ra_data = list(zip(RA_site_list, href_list))
    return render_template('species.html', species_ra_info=RA_dict, species=species_info, selected_species=selected_species, ra_data=ra_data, RA_site_list=RA_site_list, href_list=href_list, names_dict=names_dict)

if __name__ == "__main__":
    names_dict, static_url_path, gen_spec_info_dict, RA_dict, supply_table_html = marigold_boot_req.main()
    app.static_url_path=static_url_path
    app.config['NAMES_DICT'] = names_dict
    app.run()
    
