
class FlaskAppWrapper(object):
    """
    This class if usefull for add_endpoint to add end_endpoint for a flask application without python decorator
    Initialize FlaskAppWrapper with a Flask app and optional configs
    """
    def __init__(self, app, **configs):
        #Set Flask app
        self.app = app
        # Set the configurations for the app
        self.configs(**configs)

    # Configure the app with the given configs
    def configs(self, **configs):
        for config, value in configs:
            self.app.config[config.upper()] = value

    # Add an endpoint to the Flask app
    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        # Add the endpoint to the app's URL rules
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    # Start the Flask app with the given parameters
    def run(self, **kwargs):
        self.app.run(**kwargs)


