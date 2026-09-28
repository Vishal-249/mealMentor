$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open('c:\Users\Visha\Downloads\mealmentor\MealMentor_Project_Documentation\IEEE_Research_Paper\MealMentor_IEEE_Conference_Paper.docx')
$pages = $doc.ComputeStatistics(2)
$doc.Close([ref]$false)
$word.Quit()
Write-Host "EXACT PAGE COUNT IN MS WORD: $pages"
