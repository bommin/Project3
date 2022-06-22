function subselect(object){
    value = object.value
    var kia = ['K5', '스포티지', '쏘렌토', '봉고', '카니발', 'K9', '모닝', 'K7', '모하비', '리오','쏘울', '포텐샤', 'K3', '포르테', '프라이드', '옵티마리갈', '레이', '카렌스', '로체', '니로', '오피러스', '셀토스', '카스타', '스팅어', '스토닉', 'K8', '비스토터보', '쎄라토']
    var hyundai = ['그랜저', '쏘나타', '스타렉스', '포터', '투싼', '에쿠스', '베라크루즈', '갤로퍼', '싼타페','그레이스', '아반떼', '벨로스터', '맥스크루즈', '아슬란', 'i30', '코나', '엑센트', '베르나','i40', '테라칸', '투스카니', '펠리세이드', '트라제', '캐스퍼', '다이너스티', '베뉴', '뉴클릭','아이오닉']
    var renault = ['SM6', 'SM5', 'QM3', 'SM7', 'QM6', 'SM3', 'QM5', '클리오', 'XM3','마스터 밴']
    var genesis = ['EQ900', 'G80', 'G70', 'G90', 'GV80', 'GV70', 'BH330', 'DHG330', 'DHG380', 'BH380', '제네시스 쿠페']
    var chevrolet = ['크루즈', '스파크', '윈스톰', '라보', '마티즈', '올란도', '트랙스', '아베오', '라세티', '캡티바', '젠트라', '다마스', '토스카', '말리부', '알페온', '트레일블레이저', '레조', '임팔라', '카마로', '이쿼녹스', '콜로라도', '트래버스']
    var ssangyong = ['렉스턴', '액티언', '티볼리', '코란도', '체어맨', '무쏘', '카이런', '로디우스']
    var target = document.getElementById('simple');
    
    if(object.value =='기아') var d = kia;
    else if(object.value =='현대') var d = hyundai;
    else if(object.value =='르노코리아') var d = renault;
    else if(object.value=='제네시스') var d = genesis;
    else if(object.value=='쌍용') var d = ssangyong;
    else if(object.value=='쉐보레') var d = chevrolet;

    target.options.length = 0;
    for (x in d){
        var opt = document.createElement('option');
        opt.value = d[x];
        opt.innerHTML = d[x];
        target.appendChild(opt);
    }
    target.style.display = '';

}

