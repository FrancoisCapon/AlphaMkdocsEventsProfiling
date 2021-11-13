# from mkdocs.plugins import BasePlugin
import mkdocs.plugins
import mkdocs.config


# https://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback

import inspect, time, tracemalloc, os

class EventsProfiling(mkdocs.plugins.BasePlugin):

    config_scheme = (
        ('title', mkdocs.config.config_options.Type(str, default='Profiling Title')),
    )

    # https://www.mkdocs.org/dev-guide/plugins/
    def __init__(self):
        self.last_thread_time = 0
        self.event_id = 0
        tracemalloc.start()
        # gc.disable()

    def log_event(self, event_name, event_object = '', delta_time_calculable = 1):
        new_thread_time = time.thread_time()
        malloc_current, malloc_max = tracemalloc.get_traced_memory()
        event_name = event_name[3:]
        # delta_time = (new_thread_time - self.last_thread_time) * delta_time_calculable
        self.last_thread_time = new_thread_time
        self.log_file.write(f"{self.event_id}\t{self.last_thread_time:.3f}\t{malloc_current/1024:.0f}\t{malloc_max/1024:.0f}\t{event_name}\t{event_object}" + os.linesep)
        self.event_id +=1

    # Global Events 
    # https://www.mkdocs.org/dev-guide/plugins/#global-events

    def on_serve(self, server, config, builder):
        # event code
        # self.log_event(inspect.currentframe().f_code.co_name)
        return server

    def on_config(self, config):
        # event code
        self.timestamp = time.time_ns()//1000000000
        self.log_filename = os.path.dirname(config['docs_dir']) + os.sep + 'fc-events-profiling' + os.sep + str(self.timestamp) + '.log' 
        self.log_file = open(self.log_filename, 'w')
        # self.log_file.write("time\ttime\tmalloc\tmalloc\tevent" + os.linesep)
        # self.log_file.write("thread\tdelta\tcurrent\tmax\tname" + os.linesep)
        # self.log_file.write("second\tsecond\tKB\tKB\t" + os.linesep)
        # self.log_file.write(os.linesep)
        self.log_file.write(self.config['title'] + os.linesep)
        self.log_event(inspect.currentframe().f_code.co_name, delta_time_calculable = 0)
       
        return config

    def on_pre_build(self, config):
        # event code
        self.log_event(inspect.currentframe().f_code.co_name)
        return

    def on_files(self, files, config):
        # event code
        self.log_event(inspect.currentframe().f_code.co_name)
        return files

    def on_nav(self, nav, config, files):
        # event code
        self.log_event(inspect.currentframe().f_code.co_name)
        return nav

    def on_env(self, env, config, files):
        # event code
        self.log_event(inspect.currentframe().f_code.co_name)
        return env

    def on_post_build(self, config):
        # event code
        self.log_event(inspect.currentframe().f_code.co_name)
        tracemalloc.stop()
        self.log_file.close()
        return

    def on_build_error(self, error):
        # event code
        self.log_event(inspect.currentframe().f_code.co_name)
        return

    # Template Events
    # https://www.mkdocs.org/dev-guide/plugins/#template-events

    def on_pre_template(self, template, template_name, config):
        # event code
        self.log_event(inspect.currentframe().f_code.co_name, template_name)
        return template

    def on_template_context(self, context, template_name, config):
        # event code
        self.log_event(inspect.currentframe().f_code.co_name)
        return context
    
    def on_post_template(self, output_content, template_name, config):
        # event code
        self.log_event(inspect.currentframe().f_code.co_name)
        return output_content

    # Page Events
    # https://www.mkdocs.org/dev-guide/plugins/#page-events
    
    def on_pre_page(self, page, config, files):
        # event code
        self.log_event(inspect.currentframe().f_code.co_name, page.url)
        return page

    def on_page_read_source(self, page, config):
        # event code
        self.log_event(inspect.currentframe().f_code.co_name)
        return None

    def on_page_markdown(self, markdown, page, config, files):
        # event code
        self.log_event(inspect.currentframe().f_code.co_name)
        return markdown

    def on_page_content(self, html, page, config, files):
        # event code
        self.log_event(inspect.currentframe().f_code.co_name)
        # page.markdown = None # OUI
        return html

    def on_page_context(self, context, page, config, nav):
        # event code
        self.log_event(inspect.currentframe().f_code.co_name, page.url)
        # page.is_homepage()
        return context

    def on_post_page(self, output_content, page, config):
        # event code
        self.log_event(inspect.currentframe().f_code.co_name)
        return output_content
