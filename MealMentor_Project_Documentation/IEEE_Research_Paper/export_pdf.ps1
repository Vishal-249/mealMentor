$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $docPath = 'c:\Users\Visha\Downloads\mealmentor\MealMentor_Project_Documentation\IEEE_Research_Paper\MealMentor_IEEE_Conference_Paper.docx'
    $pdfPath = 'c:\Users\Visha\Downloads\mealmentor\MealMentor_Project_Documentation\IEEE_Research_Paper\MealMentor_IEEE_Conference_Paper.pdf'
    $doc = $word.Documents.Open($docPath)
    $pages = $doc.ComputeStatistics(2)
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close([ref]$false)
    Write-Host "WORD COMPUTED PAGES: $pages"
    Write-Host "PDF SAVED TO: $pdfPath"
} finally {
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
