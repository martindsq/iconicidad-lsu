from dbsettings import Group, PositiveIntegerValue

class IconicitiesOptions(Group):
	online_timeout = PositiveIntegerValue(default = 10, help_text="En minutos")
	online_sample_size = PositiveIntegerValue(default = 90)

	offline_timeout = PositiveIntegerValue(default = 20, help_text="En minutos")
	offline_sample_size = PositiveIntegerValue(default = 180)

	debug_timeout = PositiveIntegerValue(default = 1, help_text="En minutos")
	debug_sample_size = PositiveIntegerValue(default = 3)
