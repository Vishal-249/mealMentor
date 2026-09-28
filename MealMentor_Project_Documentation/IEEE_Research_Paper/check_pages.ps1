$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open("c:\Users\Visha\Downloads\mealmentor\MealMentor_Project_Documentation\IEEE_Research_Paper\MealMentor_IEEE_Conference_Paper.docx")
    $pages = $doc.ComputeStatistics(2)
    Write-Output "EXACT_PAGE_COUNT: $pages"
    $doc.Close([ref]0)
} finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
