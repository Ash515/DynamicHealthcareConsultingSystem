function solution(){
    a=document.getElementById('issues').value;
    if(a=='Cold'){
        cold_sol="Have some ginger and black pepper along with your food.😊";
        document.getElementById('textarea').value=cold_sol;
    }
    else if(a=='Fever'){
        fever_sol="Have some coconut along with your food dont eat chicken and crab.🤩";
        document.getElementById('textarea').value=fever_sol;
    }
    else if(a=='Stomach Pain'){
        stomach_sol="Drink some water and have some cold food.😎";
        document.getElementById('textarea').value=stomach_sol;
    }
    else if(a=='Head Ache'){
        headache_sol="Apply painkiller at your head and drink some tea with ginger.😉";
        document.getElementById('textarea').value=headache_sol;
    }
    else if(a=='Vomit'){
        vomit_sol="Drink some lemon juice.😁";
        document.getElementById('textarea').value=vomit_sol;
    }
     else if(a=='Acidity'){
        acidity_sol="Eat some jaggery, Lemon.Dont eat junk foods. 😚";
        document.getElementById('textarea').value=acidity_sol;
    }
    else if(a=='Tooth Pain'){
        toothpain_sol="Drink some hot water.Wash your mouth with salt. keep ginger piece or salt at the infection part 😁";
        document.getElementById('textarea').value=toothpain_sol;
    }
     else if(a=='Hairfall'){
        hairfall_sol="Dont make your head to dry and apply some pure coconut oil or ginglly oil 🌟";
        document.getElementById('textarea').value=hairfall_sol;
    }
    else if(a=='Eye Irritation'){
        eyeirritate_sol="Drink some cool juices, coconut and apply oil in your head. Dont see Television, Mobile phones, Laptops etc.😉";
        document.getElementById('textarea').value=eyeirritate_sol;
    }
     else if(a=='Obisity'){
        obisity_sol="Eat limited food dont eat junks and oil rich food. Excersise daily and do cycling.⚽";
        document.getElementById('textarea').value=obisity_sol;
    }
       else if(a=='Pimple'){
        pimple_sol="Dont eat oil rich foods, clean your face regularly with cool or hot water.😉";
        document.getElementById('textarea').value=pimple_sol;
    }
     else if(a=='Loosemotion'){
        loosemotion_sol=" Taking anti-diarrheal medications. consuming more fiber.staying hydrated.Adding honey to your diet. Avoiding food and drinks that are triggers.Taking anti-diarrheal medications.🌟";
        document.getElementById('textarea').value=loosemotion_sol;
    }
     else if(a=='Diabetes'){
        diabetes_sol="Dont eat Egg and red meat. Dont take more sugar content rich foods. Eat blueberry and whaet rich cookies.";
        document.getElementById('textarea').value=diabetes_sol;
    }
 }