$.get('/api/TravelInfo', function (Data) {
    for (var i = 0; i < 25; i++) {
        var RowData = Data[i];
        $('#a'+RowData['Type']+' > #card-container').append('<div class="max-w-sm bg-white rounded-lg border border-gray-200 shadow-xl dark:bg-gray-800 dark:border-gray-700"><a href="#"><img class="rounded-t-lg" src="'+RowData['ImageUrl']+'" alt="" /></a><div class="p-4"><a href="#"><h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">'+ RowData['Title']+'</h5></a><p>'+RowData['EventTime']+'</p><p class="mb-3 font-normal text-gray-700 dark:text-gray-400">人數限制：'+RowData['Quota']+' 人</p><p class="mb-3 font-normal text-gray-700 dark:text-gray-400">$'+ RowData['Price']+' 起</p><a href="#" class="inline-flex items-center py-2 px-3 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">了解詳情<svg class="ml-2 -mr-1 w-4 h-4" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg></a></div></div>');
    }
    for (var j = 0; j < 3; j++) {
        var RowData = Data[j];
        $("#carouselExampleControls" + " .carousel-indicators").append('<button type="button" data-bs-target="#carouselExampleControls' + '" data-bs-slide-to="' + j + '" aria-label="Slide ' + j + '"></button>');
        $('#carouselExampleControls'+' .carousel-inner').append('<div class="carousel-item"><img src="' + RowData['ImageUrl'] + '" class="d-block w-100 object-cover"><div class="carousel-caption d-none d-md-block bottom-36">' +'<h3 class="text-5xl drop-shadow-md font-bold">'+ RowData['Title'] + '</h3><p class="text-2xl font-bold">只需 '+RowData['Price']+' 起</p>');
        
    }
    document.querySelector('#carouselExampleControls > div.carousel-inner > div:nth-child(1)').classList.add("active"); 
    document.querySelector('#carouselExampleControls > div.carousel-indicators > button:nth-child(1)').classList.add("active"); 
});