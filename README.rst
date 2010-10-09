=================
Purplescript
=================


Purplescript is small ruby like language written in Python that compiles to PHP



 Syntax
============

   /// VARIABLES
   
   /* PHP */
   $test = 'Example';


	/* Purplescript */
	test = 'Example'



	/// CONSTANTS


	/* PHP */
	define('TEST', 'constant');

	/* Purplescript */
	TEST = 'constant'


	/// OBJECT ORIENTED STUFF
	
	
	/* PHP */
	$this->something->another_thing = something_else;



	/* Purplescript */
	@something.another_thing = something_else


	/// ARRAYS
	

	/* PHP */
	$store_data = array
	(
		'product_name' => $this->input->post('product_name'),
		'active' => $this->input->post('active'),
	);

	$simple_array = array
	(
		'element', 'element2', 'element3'

	);


	/* Purplescript */
	store_data =
	{

		'product_name' : @input.post('product_name'),
		'active' : @input.post('active)

	}

	simple_array =
	{

		'element', 'element2', 'element3'

	}





	// CONTROL FLOWS
	
	
	/* Purplescript */
	for key, value in store

		echo key

	endfor


	if(expression)

	elseif(expression)

	else


	endif





	// FUNCTIONS
	
	
	/* PHP */
	function Example()
	{
		parent::Controller();
		$this->load->model('parent');

	}

	function add_product()
	{

		$this->data['store'] = $this->stores_model->get_store_by_id(store_id);


	}


	/* Purplescript */
	def Example()

		parent::My_controller()
		@load.model('parent')


	end

	def add_product()

		@data['store'] = @stores_model.get_store_by_id(store_id)

	end
	
	
	// CLASSES
	

    class Example extends Controller
	endclass