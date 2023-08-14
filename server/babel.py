import os
import subprocess
from flask import request, session, jsonify
from flask_babel import Babel
from g4f import Provider
import re
from g4f.models import Model, ModelUtils


def get_languages_from_dir(directory):
    """Return a list of directory names in the given directory."""
    return [name for name in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, name))]

def get_model_relations():
    # breakpoint()
    model_relations = {
        "prov_to_model": {},
        "model_to_prov": {},
        "providers": {}
    }
    for name, cls in Provider.__dict__.items():
        if cls is None or re.search(r'(?:Provider|__)', name):
            continue
        model_relations['providers'][name] = cls

        if (type(cls.model) is str):
            cls.model = [cls.model]

        model_relations["prov_to_model"][name] = cls.model
        for model in cls.model:
            if model not in model_relations["model_to_prov"]:
                model_relations["model_to_prov"][model] = []
            model_relations["model_to_prov"][model].append(name)
        
        model_relations['model_to_prov'] = dict(sorted(model_relations['model_to_prov'].items(), key=lambda i: i[0].lower()))
    return model_relations

BABEL_DEFAULT_LOCALE = 'en_US'
BABEL_LANGUAGES = get_languages_from_dir('translations')
BABEL_MODEL_RELATIONS = get_model_relations()

def create_babel(app):
    """Create and initialize a Babel instance with the given Flask app."""
    babel = Babel(app)
    app.config['BABEL_DEFAULT_LOCALE'] = BABEL_DEFAULT_LOCALE
    app.config['BABEL_LANGUAGES'] = BABEL_LANGUAGES
    app.config['BABEL_MODEL_RELATIONS'] = BABEL_MODEL_RELATIONS

    babel.init_app(app, locale_selector=get_locale)
    compile_translations()


def get_locale():
    """Get the user's locale from the session or the request's accepted languages."""
    return session.get('language') or request.accept_languages.best_match(BABEL_LANGUAGES)


def get_languages():
    """Return a list of available languages in JSON format."""
    return jsonify(BABEL_LANGUAGES)

def get_providers_by_model(model):
    return list(BABEL_MODEL_RELATIONS['model_to_prov'][model])

def get_models_by_provider(provider):
    try:
        return list(BABEL_MODEL_RELATIONS['prov_to_model'][provider])
    except Exception:
        return []
    

def get_best_provider_by_model(model):
    try:
        m = ModelUtils.convert[model]
        return re.search(r'Providers\.(.*)', m.best_provider.__name__)[1]
    except Exception:
        return "None"

def get_provider_by_name(name):
    if name is None or name == 'BEST':
        return None
    else:
        return BABEL_MODEL_RELATIONS['providers'][name]

def get_all_models():
    return list(BABEL_MODEL_RELATIONS['model_to_prov'].keys())

def compile_translations():
    """Compile the translation files."""
    result = subprocess.run(
        ['pybabel', 'compile', '-d', 'translations'],
        stdout=subprocess.PIPE,
    )

    if result.returncode != 0:
        raise Exception(
            f'Compiling translations failed:\n{result.stdout.decode()}')

    print('Translations compiled successfully')
