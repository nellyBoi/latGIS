"""
Nelly Kane
11.08.2019

Running IPView from the command line.
"""
import setup_ipview


########################################################################################################################
def run() -> object:
    """
    """
    setup_ipview.setup()

    # import after setup
    import ip_view_ui.ipview_viewer as view
    application = view.launch()

    return application


########################################################################################################################
if __name__ == '__main__':

    runner = run()
