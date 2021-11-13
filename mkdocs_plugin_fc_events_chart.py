import matplotlib.pyplot as pyplot # need installation
# from matplotlib.patches import Rectangle
#from matplotlib import collections 
import csv, sys

class ProfilingEvent():
       
    def __init__(self, id, name, time_thread, malloc, malloc_max, object_name):
        self.id, self.name, self.time_thread, self.type = int(id), name, float(time_thread), type
        self.malloc, self.malloc_max, self.object  = float(malloc)/1024, float(malloc_max)/1024, object_name
        self.type = self.get_type() 

    def get_type(self):
        if 'page' in self.name:
            return 'page'
        elif 'template' in self.name:
            return 'template'
        return 'global'

class ProfilingEvents():
   
    CSV_ID, CSV_TIME, CSV_MALLOC, CSV_MALLOC_MAX = 0, 1, 2, 3
    CSV_EVENT_NAME, CSV_OBJECT_NAME = 4, 5

    def __init__(self, log_filename):
        phase_current = ''
        phase_index = -1
        self.data = [] # phases > events
        with open(log_filename, newline='') as logfile:
            logreader = csv.reader(logfile, delimiter='\t')
            self.title = next(logreader)[0]
            for row in logreader:
                id = int(row[self.CSV_ID])
                name = row[self.CSV_EVENT_NAME]
                time_thread = row[self.CSV_TIME]
                malloc = row[self.CSV_MALLOC]
                malloc_max = row[self.CSV_MALLOC_MAX]
                try:
                    object_name = row[self.CSV_OBJECT_NAME]
                except:
                    object_name = None
                event = ProfilingEvent(id, name, time_thread, malloc, malloc_max, object_name)
                if event.type != phase_current:
                    phase_current = event.type
                    phase_index += 1
                    self.data.append([]) # new phase
                self.data[phase_index].append(event)
        #print(self.title, self.data)

class MemoryAllocationGraph():

    def __init__(self, profiling_events, mathplot_area, phase_plot_default_options = {}, phases_plot_options = [{},{},{},{},{},{}], phase_only = False):
      
        phase_index = -1
        y_malloc = mathplot_area.gca()
        for phase in profiling_events.data:
            phase_index += 1
            malloc = []
            event_first = phase[0] 
            x_items = range(event_first.id, event_first.id + len(phase))
            # https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression-taking-union-of-dictiona
            plot_options = {**phase_plot_default_options, **phases_plot_options[phase_index]}
            for event in phase:
                malloc.append(event.malloc)
            y_malloc.axvline(event_first.id, 0, 1, color = 'grey', linestyle = '--', linewidth=1) 
            y_malloc.plot(x_items, malloc, **plot_options)
        if not phase_only:    
            mathplot_area.ylabel('memory (KB)')
            y_malloc.tick_params(labelbottom=True,labeltop=True,labelleft=True,labelright=True)
            y_malloc.axvline(event_first.id, 0, 1, color = 'grey', linestyle = '--', linewidth=1) 
            mathplot_area.grid(True)
            mathplot_area.title('Mkdocs Malloc Proflinig: ' + profiling_events.title, fontsize=20, pad=20)
        else:
            mathplot_area.title(y_malloc.get_title() + ' vs ' + profiling_events.title, fontsize=20, pad=20)
        
        #mathplot_area.plot(time_thread)



if __name__ == '__main__':
    events = ProfilingEvents(sys.argv[1])
    area = pyplot
    area.figure("Mkdocs Malloc Profiling", figsize=(15, 9))
    area.subplots_adjust(left=0.05, right=0.95)
    phase_plot_default_options = {'marker':'', 'markersize':'3', 'drawstyle':'steps','markevery':100, 'color':'grey'}
    phases_plot_options = []
    phases_plot_options.append({}) # global 1
    phases_plot_options.append({'markevery':4, 'color':'deepskyblue'}) # page 1
    phases_plot_options.append({}) # global 2
    phases_plot_options.append({'markevery':3}) # template
    phases_plot_options.append({'markevery':2, 'color':'deepskyblue'}) # page 2
    phases_plot_options.append({}) # global 3
    MemoryAllocationGraph(events, area, phase_plot_default_options, phases_plot_options)
    if len(sys.argv) > 2:
        events = ProfilingEvents(sys.argv[2])
        phases_plot_options[1]= {'markevery':4, 'color':'darkorange'} # page 1
        phases_plot_options[4]= {'markevery':2, 'color':'darkorange'} # page 2
        MemoryAllocationGraph(events, area, phase_plot_default_options, phases_plot_options, True)
    area.show()
    area.close()


        

# https://stackoverflow.com/questions/24988448/how-to-draw-vertical-lines-on-a-given-plot-in-matplotlib

# https://matplotlib.org/stable/gallery/color/named_colors.html#sphx-glr-gallery-color-named-colors-py

class Graph():

    def get_even_type(self, event):
        if 'page' in event:
            return 'page'
        elif 'template' in event:
            return 'template'
        return 'global'

    def __init__(self, log_filename_one = None):

        event_type_color = { 'page':'green', 'template':'grey', 'global':'grey'}

        if not log_filename_one:
            log_filename_one = sys.argv[1]  
        # data_one_malloc_segment= []
        #data_one_time_segments= []
        data_one_malloc_segments= []
        date_one_event_type_segments = []
        #data_one_malloc =[]
        data_one_time = []
        data_one_malloc_max = []
        data_current_event_type = ''
        #data_current_event_type_start_id = 1
        data_current_event_id = 0
        data_current_segment_id = -1
        
        pyplot.figure(figsize=(20, 5))
        pyplot.subplots_adjust(left=0.05, right=0.95)
        
        with open(log_filename_one, newline='') as logfile:
            logreader = csv.reader(logfile, delimiter='\t')
            self.title = next(logreader)[0]
            for row in logreader:
                #data_one_time.append(float(row[0]))
                # data_one_malloc.append(int(row[1]))
                # data_one_malloc_max.append(int(row[2]))
                #if event_type != data_current_event_type:
                    #pyplot.axvline(data_current_event_id, color=event_type_color[event_type])
                    # pyplot.axvspan(data_current_event_type_start_id - 1,data_current_event_id -0.5 , color=event_type_color[data_current_event_type])
                    # data_current_event_type = event_type
                    # data_current_event_type_start_id = data_current_event_id
                event = row[4]
                event_type = self.get_even_type(event)
                if event_type != data_current_event_type:
                    #data_one_time_segments.append([])
                    data_one_malloc_segments.append([])
                    date_one_event_type_segments.append(event_type)
                    data_current_segment_id += 1
                    data_current_event_type = event_type    
                # data_one_time_segments[data_current_segment_id].append(float(row[0]))
                data_one_time.append(float(row[1]))
                data_one_malloc_segments[data_current_segment_id].append(int(row[2]))
                data_one_malloc_max.append(int(row[3]))
                data_current_event_id += 1
            # print(data_one_time_segments,date_one_event_type_segments )
            # https://matplotlib.org/stable/gallery/ticks_and_spines/multiple_yaxis_with_spines.html
            #y_malloc = pyplot.twinx()
            pyplot.title = (self.title + "hello")

            y_malloc = pyplot.gca()
            pyplot.ylabel('memory (KB)')

            ticks_major = range(0, len(data_one_time) +1, 50)
            ticks_minor = range(0, len(data_one_time) +1, 10)
            # y_malloc.set_xticks(ticks_major)
            # y_malloc.set_xticks(ticks_minor, minor=True)

            pyplot.grid(True)
            legend_lines = []
            y_malloc.set_zorder(1)
            # https://stackoverflow.com/questions/51445002/subplot-axis-set-zorder-plots-dissapear
            y_malloc.set_facecolor("none")


            pyplot.twinx().set_zorder = 0
            pyplot.ylabel('time (s)')
            #tx = range(1, len(data_one_time) + 1)
            # https://stackoverflow.com/questions/11983024/matplotlib-legends-not-working
            legend_line, = pyplot.plot(data_one_time, 's-', markersize=0, color='blue', label="time", drawstyle='steps', linewidth=1)
            legend_lines.append(legend_line)

            
            #y_malloc.legend()
            legend_line, = y_malloc.plot(data_one_malloc_max, ls=":",color='grey', linewidth = 1, label="malloc max", drawstyle='steps')
            legend_lines.append(legend_line)



            # y_time = pyplot.twinx()
            # y_time.plot(data_one_time_segments[0])
            # x_start = len(data_one_time_segments[0])
            # x_length = len(data_one_time_segments[1])
            # pyplot.plot(range(x_start,x_start + x_length),data_one_time_segments[1])
            x_start = 0
            for i in range(0, len(data_one_malloc_segments)):
                # time_segment = data_one_time_segments[i]
                malloc_segment = data_one_malloc_segments[i]
                event_type = date_one_event_type_segments[i]
                color = event_type_color[event_type]
                x_length = len(malloc_segment)
                # y_time.plot(range(x_start,x_start + x_length),time_segment, 'o-', color=color)
                legend_line, =  y_malloc.plot(range(x_start,x_start + x_length), malloc_segment, color=color, label = 'malloc for ' + event_type, linewidth=1, drawstyle='steps', marker='o', markevery=2, markersize=3)
                legend_lines.append(legend_line)
                x_start += x_length
            
            
            tmp_template = legend_lines[5]
            tmp_page = legend_lines[3]
            tmp_global = legend_lines[2]
            tmp_time = legend_lines[0]
            tmp_malloc_max = legend_lines[1]
            legend_lines = []
            legend_lines.append(tmp_global)
            legend_lines.append(tmp_page)
            legend_lines.append(tmp_template)
            legend_lines.append(tmp_malloc_max)
            legend_lines.append(tmp_time)
            y_malloc.legend(handles=legend_lines,loc='upper left', ncol=len(legend_lines))
            #print(self.title)
            pyplot.show()
            # pyplot.axvspan(data_current_event_type_start_id - 1,data_current_event_id -0.5 , color=event_type_color[data_current_event_type])
        # pyplot.axvspan(0,20,color='lavender')
 # Create a figure containing a single axes.
    # # ax.plot([1, 2, 3, 4], [1, 4, 2, 3])  # Plot some data on the axes.
    
        # pyplot.show()
    # def plot(profiling):
    # # fig, ax = pyplot.subplots()  # Create a figure containing a single axes.
    # # ax.plot([1, 2, 3, 4], [1, 4, 2, 3])  # Plot some data on the axes.
    # # pyplot.show()
    # data_time= []
    # data_time_delta= []
    # data_malloc =[]
    # data_malloc_max =[]
    # with open(profiling.log_filename, newline='') as logfile:
    #     logreader = csv.reader(logfile, delimiter='\t')
    #     for row in logreader:
    #         data_time.append(float(row[0]))
    #         data_time_delta.append(float(row[1]))
    #         data_malloc.append(int(row[2])/1024)
    #         data_malloc_max.append(int(row[3])/1024)


       
    #     pyplot.figure(figsize=(10, 3))
    #     pyplot.scatter(x=data_time, y=data_time)
    #     pyplot.plot(data_time, data_time)
    #     pyplot.plot(data_time, data_malloc_max)
    #     pyplot.scatter(data_time, data_time_delta)
    #     pyplot.scatter(data_time, data_malloc)
       
    #     pyplot.show()

    #     # color = 'lightgrey'
    #     # times_axe.set_ylabel('time (s)', color=color)
    #     # times_axe.tick_params(axis='y', labelcolor=color)
    #     # times_axe.plot(data_time)

    #     # color = 'tab:orange'
    #     # malloc_axe = times_axe.twinx()tw  # instantiate a second axes that shares the 
    #     # malloc_axe.set_ylabel('malloc (KB)', color=color)
    #     # malloc_axe.tick_params(axis='y', labelcolor=color)
    #     # malloc_axe.plot(data_malloc, color=color)

    #     # color = 'tab:blue'
    #     # ax2.set_ylabel('sin', color=color)  # we already handled the x-label with ax1
    #     # ax2.plot(t, data2, color=color)
    #     # ax2.tick_params(axis='y', labelcolor=color)
    #     # figure.tight_layout()
    #     # figure.subplots_adjust(bottom=0.1)




    #     #print(data_malloc)
    #     # pyplot.plot(data_time)
    #     # pyplot.plot(data_malloc)
    #     # pyplot.ylabel('KB')
    #     # pyplot.xlabel('event id')
    #     # pyplot.show()

# if __name__ == '__main__':
#     graph = Graph()