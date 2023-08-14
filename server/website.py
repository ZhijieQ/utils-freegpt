from flask import render_template, redirect, url_for, request, session
from flask_babel import refresh
from time import time
from os import urandom
from server.babel import get_locale, get_languages, get_providers_by_model, get_models_by_provider, get_best_provider_by_model, get_all_models

class Website:
    def __init__(self, bp, url_prefix) -> None:
        self.bp = bp
        self.url_prefix = url_prefix
        self.routes = {
            '/': {
                'function': lambda: redirect(url_for('._index')),
                'methods': ['GET', 'POST']
            },
            '/chat/': {
                'function': self._index,
                'methods': ['GET', 'POST']
            },
            '/chat/<conversation_id>': {
                'function': self._chat,
                'methods': ['GET', 'POST']
            },
            '/change-language': {
                'function': self.change_language,
                'methods': ['POST']
            },
            '/get-locale': {
                'function': self.get_locale,
                'methods': ['GET']
            },
            '/get-languages': {
                'function': self.get_languages,
                'methods': ['GET']
            },
            '/get-providers_by_model': {
                'function': self.get_providers_by_model,
                'methods': ['POST']
            },
            '/get-models_by_provider': {
                'function': self.get_models_by_provider,
                'methods': ['POST']
            },
            '/get-best_provider_by_model': {
                'function': self.get_best_provider_by_model,
                'methods': ['POST']
            },
            '/get-all_models': {
                'function': self.get_all_models,
                'methods': ['GET']
            },
        }

    def _chat(self, conversation_id):
        if '-' not in conversation_id:
            return redirect(url_for('._index'))

        return render_template('index.html', chat_id=conversation_id, url_prefix=self.url_prefix)

    def _index(self):
        return render_template('index.html', chat_id=f'{urandom(4).hex()}-{urandom(2).hex()}-{urandom(2).hex()}-{urandom(2).hex()}-{hex(int(time() * 1000))[2:]}', url_prefix=self.url_prefix)

    def change_language(self):
        data = request.get_json()
        session['language'] = data.get('language')
        refresh()
        return '', 204

    def get_locale(self):
        return get_locale()
    
    def get_languages(self):  
        return get_languages()

    def get_providers_by_model(self):
        return get_providers_by_model(request.json['model'])

    def get_models_by_provider(self):
        return get_models_by_provider(request.json['provider'])

    def get_best_provider_by_model(self):
        return get_best_provider_by_model(request.json['model'])

    def get_all_models(self):
        return get_all_models()