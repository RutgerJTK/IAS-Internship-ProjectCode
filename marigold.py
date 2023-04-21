from flask import Flask, render_template, request
import marigold_boot_req

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('index.html', species_dict=gen_spec_info_dict, RA_info_dict=RA_dict )


@app.route('/species/<species_name>')
def species_page(species_name):
    selected_species = request.args.get('selected_species')
    species_info = gen_spec_info_dict.get(species_name)
    # species_risk_info = request.args.get('species_risk_info')
    species_risk_info = RA_dict.get(names_dict[species_name])
    print(species_name)
    print(species_info)
    return render_template('species.html', species_ra_info=RA_dict, species=species_info, selected_species=selected_species, names_dict=names_dict)

if __name__ == "__main__":
    names_dict, static_url_path, gen_spec_info_dict, RA_dict = marigold_boot_req.main()
    print(names_dict)
    app.static_url_path=static_url_path
    app.config['NAMES_DICT'] = names_dict
    app.run()
    
