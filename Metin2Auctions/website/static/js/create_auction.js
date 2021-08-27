function hide(element){
    element.classList.add('hide')
}
function show(element){
    element.classList.remove('hide')
}
function choose_category(element){
    let option = element.options[element.selectedIndex].text;
    let item_form = document.querySelector('section.item');
    switch(option){
        case 'Item':
            show(item_form);
            break;
        default:
            hide(item_form);
    }
}
function check_number(element){
    option = element.value;
    let item_form = document.querySelectorAll('label.bonus');
    let border = document.querySelector('.bonus_names');
    for(let i = 7; i>option;i--){
        hide(item_form[i]);
    }
    for(let i = 0; i<=option;i++){
        show(item_form[i])
    }
    if(option==0) border.style.display="none";
    else border.style.display="flex";
}
function weapon(element){
    option = document.querySelector('.element')
    if (element.checked == true) show(option);
    else hide(option);
}