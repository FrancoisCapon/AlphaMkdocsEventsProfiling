from setuptools import setup

setup(
    name="mkdocs-plugin-fc-events-profiling",
    version="0.0.1",
    py_modules=["mkdocs_plugin_fc_events_profiling","mkdocs_plugin_fc_events_chart"],
    entry_points={
        'mkdocs.plugins': [
        'fc_events_profiling = mkdocs_plugin_fc_events_profiling:EventsProfiling',
        ]
}
)