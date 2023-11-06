from django.forms import CheckboxSelectMultiple, RadioSelect


class CustomCheckboxMultiple(CheckboxSelectMultiple):
    """
    Переопределяет шаблон для CheckboxSelectMultiple

    """
    option_template_name = 'store/filter-template-for-checkbox-widgets.html'


class CustomRadioSelect(RadioSelect):
    """
    Переопределяет шаблон для RadioSelect
    """
    option_template_name = 'store/filter-template-for-checkbox-widgets.html'
