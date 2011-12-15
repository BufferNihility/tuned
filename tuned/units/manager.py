import tuned.exceptions
import tuned.logs
import tuned.patterns
import tuned.units.unit

log = tuned.logs.get()

class UnitManager(tuned.patterns.Singleton):
	"""
	UnitManager is a singleton, instantiates all Unit objects, and keeps track of them.
	"""

	__slots__ = ["_units"]

	def __init__(self):
		super(self.__class__, self).__init__()
		self._units = set()

	@property
	def units(self):
		return self._units.copy()

	def create(self, name, plugin_name, config):
		log.info("creating unit %s" % name)
		(device, options) = self._get_plugin_params(config)
		try:
			new_unit = tuned.units.unit.Unit(name, plugin_name, [], options)
			self._units.add(new_unit)
			return new_unit
		except tuned.exceptions.TunedException as e:
			e.log()
			log.error("unable to create unit %s" % name)

	def delete(self, unit):
		assert type(unit) is tuned.units.unit.Unit
		unit.clean()
		self._units.delete(unit)

	def delete_all(self):
		for unit in self._units:
			unit.clean()
		self._units.clear()

	def _get_plugin_params(self, config):
		if config is None:
			return (None, {})

		assert type(config) is dict
		if "devices" in config:
			devices = config[devices].strip().split()
			if len(devices) == 0:
				devices = None
			del(config["devices"])

		return (devices, config)
