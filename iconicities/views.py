from django.http import HttpResponse
from django.template import loader
from django.templatetags.static import static
from django.utils.translation import gettext as _
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from .models import Form, Stimulus
from .apps import IconicitiesConfig
from .serializers import FormAndRepliesSerializer, StimulusSerializer
from .permissions import IsAdminOrWriteOnly
from django.views.decorators.csrf import csrf_protect
from random import shuffle

class FormViewSet(ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormAndRepliesSerializer
    permission_classes = [IsAdminOrWriteOnly]

class StimulusViewSet(ModelViewSet):
    queryset = Stimulus.objects.all()
    serializer_class = StimulusSerializer

@csrf_protect
def index(request):
	try:
		mode = Form.Mode(int(request.GET.get('mode', 1)))
	except ValueError:
		mode = Form.Mode.ONLINE
	
	template = loader.get_template('index.html')

	options = IconicitiesConfig.options
	sample_size = options.online_sample_size if mode == Form.Mode.ONLINE else options.offline_sample_size if mode == Form.Mode.OFFLINE else options.debug_sample_size
	example_size = 3
	
	controls = list(Stimulus.objects.filter(is_active = True, is_control = True))
	variables = list(Stimulus.objects.filter(is_active = True, is_control = False))
	shuffle(variables)

	number_of_variables_to_pick = max(sample_size - len(controls), 0)
	stimuli = controls + variables[:number_of_variables_to_pick]
	examples = variables[number_of_variables_to_pick:number_of_variables_to_pick+example_size]

	context = {
    	'survey_steps': [
    		{
    			'label': '¿En qué año naciste?',
    			'hint': 'birthdate',
    			'type': 'select',
    			'required': True,
    			'options': reversed(range(1900, 2023))
    		},
    		{
    			'label': '¿Con qué género te identificás mejor?',
    			'hint': 'sex',
    			'type': 'radio',
    			'required': True,
    			'options': Form.Sex.choices
    		},
    		{
    			'label': '¿Cuál es el mayor nivel de estudios alcanzado?',
    			'hint': 'education',
    			'type': 'radio',
    			'required': True,
    			'options': Form.Education.choices
    		},
            {
    			'label': 'Del 1 al 7, ¿cómo puntuas tu fluidez con la LSU? En este estudio pueden participar personas sin conocimientos de LSU, en ese caso, podés puntuarte con 1.',
    			'hint': 'lsu_fluency',
    			'type': 'likert',
    			'required': True
    		},
    		{
    			'label': '¿Cuál es tu lengua preferida para comunicarte?',
    			'hint': 'preferred_language',
    			'type': 'radio',
    			'required': True,
    			'options': Form.PreferredLanguage.choices
    		}	
    	],
    	'stimuli': {static('terms/' + stimulus.file_name): {'filename': stimulus.file_name, 'term': stimulus.term} for stimulus in stimuli[:sample_size]},
    	'examples': {static('terms/' + example.file_name): {'filename': example.file_name, 'term': example.term} for example in examples[:example_size]},
    	'mode': mode,
    	'modes': Form.Mode,
    	'timeout': options.online_timeout if mode == Form.Mode.ONLINE else options.offline_timeout if mode == Form.Mode.OFFLINE else options.debug_timeout,
    	'sample_size': sample_size
	}
	return HttpResponse(template.render(context, request))
