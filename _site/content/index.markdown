--- 
title: Home
---

Purplescript is a small language that compiles to PHP.


# Overview




# Installation and usage



# Language reference



# Variables and constants
Constants

~~~~~~~~
TEST = 'constant'	
~~~~~~~~
{:.left_code}

~~~~~~~~
define('TEST', 'constant'); 
~~~~~~~~
{:.right_code}

Variables


~~~~~~~~~~~
test = 'Example'

@something.another_thing = something_else
~~~~~~~~~~~~
{:.left_code}


~~~~~~~~~~~~~
$test = 'Example';

$this->something->another_thing = something_else;
~~~~~~~~~~~~~
{:.right_code}


# Arrays

~~~~~~~~~~~
store_data =
{
	'product_name' : @input.post('product_name'),
	'active' : @input.post('active)
}

simple_array =
{
	'element', 'element2', 'element3'
}
~~~~~~~~~~~~
{:.left_code}


~~~~~~~~~~~~~
$store_data = array
(
	'product_name' => $this->input->post('product_name'),
	'active' => $this->input->post('active'),
);

$simple_array = array
(
	'element', 'element2', 'element3'
);
~~~~~~~~~~~~~
{:.right_code}



# Classes and functions
Classes

~~~~~~~~~~~
class Example extends Controller
endclass
~~~~~~~~~~~~
{:.left_code}

~~~~~~~~~~~~~
class Example extends Controller 
{}
~~~~~~~~~~~~~
{:.right_code}

Functions

~~~~~~~~~~~
def Example()
	parent::Controller()
	@load.model('parent')
end

def add_product(id)
	@data['store'] = @stores_model.get_store_by_id(id)
end
~~~~~~~~~~~~
{:.left_code}


~~~~~~~~~~~~~
function Example()
{
	parent::Controller();
	$this->load->model('parent');
}

function add_product($id)
{
	$this->data['store'] = $this->stores_model->get_store_by_id($id);
}
~~~~~~~~~~~~~
{:.right_code}


# Conditionals and operators


~~~~~~~~
if something is 1:
elseif something is 2:
else:
endif
~~~~~~~~
{:.left_code}

~~~~~~~~
if($something == 1)
{
}
elseif($something == 2)
{
}
else
{
}
~~~~~~~~
{:.right_code}
