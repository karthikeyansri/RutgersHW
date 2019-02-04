
Sub e_m_h()

    Dim ws As Worksheet
    Dim ws_name As String
    Dim current_ticker_symbol As String
    Dim ticker_row_start As Long
    Dim ticker_out_row_start As Long
    Dim total_ticker_volume As Double
    Dim yearly_change As Double
    Dim percent_yearly_change As Double
    Dim ticker_count As Long
    
    Dim big_tickers(2) As String
    Dim big_percent_yearly_change(1) As Double
    Dim big_ticker_volume As Double
    
    ticker_count = 0
    
    For Each ws In ActiveWorkbook.Worksheets
        NumRows = ws.Cells(Rows.Count, 1).End(xlUp).Row
        ws_name = ws.Name
        
        ticker_row_start = 2
        ticker_out_row_start = 1
        total_ticker_volume = 0
        current_ticker_symbol = ""
        big_tickers(0) = current_ticker_symbol
        big_tickers(1) = current_ticker_symbol
        big_tickers(2) = current_ticker_symbol
        big_percent_yearly_change(0) = 0#
        big_percent_yearly_change(1) = 0#
        big_ticker_volume = 0#
        Debug.Print (ws_name)
        Debug.Print ("Rows: " + Str(NumRows))
        
        ' Can be used to sort by ticker symbol. Must add some code piece that will allow to group by tcker and sort by Date. will suit this application 100%
        ' ws.Range("A1").CurrentRegion.Sort Key1:=ws.Range("A1"), order1:=xlAscending, Header:=xlYes
        
        For Row = 1 To NumRows
            If (ws.Cells(Row, 1).Value <> "<ticker>") Then
                If ((ws.Cells(Row, 1).Value <> current_ticker_symbol) Or ((ws.Cells(Row, 1).Value = current_ticker_symbol) And (Row = NumRows))) Then
                    
                    ' Update the excel with the ticker stats obtained so far
                    If ((current_ticker_symbol <> "")) Then
                        ' Debug.Print (Str(Row))
                        
                        ''' Calculation START
                        If (Row = NumRows) Then
                            total_ticker_volume = total_ticker_volume + ws.Cells(Row, 7).Value
                            Row = Row + 1
                        End If
                        ' Calculate change = year end closing price - year's opening price
                        yearly_change = ws.Cells((Row - 1), 6) - ws.Cells(ticker_row_start, 3)
                        ' % change = 100 * (year end closing price - year's opening price) / year's opening price
                        If (ws.Cells(ticker_row_start, 3) > 0) Then
                            percent_yearly_change = yearly_change / ws.Cells(ticker_row_start, 3)
                        Else
                            percent_yearly_change = 0#
                        End If
                        
                        ' Big Ticker Calculations:
                        If (big_ticker_volume < total_ticker_volume) Then
                            big_tickers(2) = current_ticker_symbol
                            big_ticker_volume = total_ticker_volume
                        End If
                        
                        If (big_percent_yearly_change(0) < percent_yearly_change) Then
                            big_tickers(0) = current_ticker_symbol
                            big_percent_yearly_change(0) = percent_yearly_change
                        ElseIf (big_percent_yearly_change(1) > percent_yearly_change) Then
                            big_tickers(1) = current_ticker_symbol
                            big_percent_yearly_change(1) = percent_yearly_change
                        End If
                        
                        ''' Calculation END
                        
                        ''' Set Excel Values START
                        ' Set ticker symbol, Change, % Change and Volume in excelsheet
                        ws.Range("I" & ticker_out_row_start).Value = current_ticker_symbol
                        ws.Range("J" & ticker_out_row_start).Value = yearly_change
                        ' Format yearly_change cell
                        If (yearly_change > 0) Then
                            ws.Range("J" & ticker_out_row_start).Interior.ColorIndex = 4
                        Else
                            ws.Range("J" & ticker_out_row_start).Interior.ColorIndex = 3
                        End If
                        ws.Range("K" & ticker_out_row_start).Value = percent_yearly_change
                        ' Format percent_yearly_change cell
                        ws.Range("K" & ticker_out_row_start).NumberFormat = "0.00%"
                        ws.Range("L" & ticker_out_row_start).Value = total_ticker_volume
                        ''' Set Excel Values END
                    End If
                    
                    ''' Reset Buffers START
                    ' Set the next output  row
                    ticker_out_row_start = ticker_out_row_start + 1
                    ' Update ticker symbol with new value
                    current_ticker_symbol = ws.Cells(Row, 1).Value
                    ' Set the ticket counter and the ticker start row for reference
                    ticker_count = ticker_count + 1
                    ticker_row_start = Row
                    ' Reset total_ticker_volume, yearly_change, percent_yearly_change values for new ticker symbol
                    total_ticker_volume = 0
                    ' Calculate volume
                    total_ticker_volume = total_ticker_volume + ws.Cells(Row, 7).Value
                    yearly_change = 0#
                    percent_yearly_change = 0#
                    ''' Reset Buffers END
                    
                Else
                    total_ticker_volume = total_ticker_volume + ws.Cells(Row, 7).Value
                End If
            Else
                set_headers (ws_name)
            End If
        Next Row
        
        Debug.Print ("ticker_count: " + Str(ticker_count))
        Debug.Print ("==================================")
        
        set_big_tickers p_big_tickers:=big_tickers, p_big_percent_yearly_change:=big_percent_yearly_change, p_big_ticker_volume:=big_ticker_volume, p_ws_name:=ws_name
        Debug.Print ("Ticker: " + big_tickers(0) + "; Greatest % increase: " + Str(big_percent_yearly_change(0)))
        Debug.Print ("Ticker: " + big_tickers(1) + "; Greatest % decrease: " + Str(big_percent_yearly_change(1)))
        Debug.Print ("Ticker: " + big_tickers(2) + "; Greatest Volume: " + Str(big_ticker_volume))
        
    Next ws
    
End Sub

Sub set_headers(ByVal ws_name As String)

    Dim ws As Worksheet
    Set ws = ActiveWorkbook.Worksheets(ws_name)
    ws.Range("I1") = "Ticker"
    ws.Range("J1") = "Yearly Change"
    ws.Range("K1") = "Percent Change"
    ws.Range("L1") = "Total Stock Volume"
    ws.Range("J:L").ColumnWidth = 20
    
    ws.Range("O2") = "Greatest % increase"
    ws.Range("O3") = "Greatest % decrease"
    ws.Range("O4") = "Greatest Total Volume"
    ws.Range("P1") = "Ticker"
    ws.Range("Q1") = "Value"
    ws.Range("O:Q").ColumnWidth = 20
End Sub

Sub set_big_tickers(p_big_tickers() As String, p_big_percent_yearly_change() As Double, p_big_ticker_volume As Double, p_ws_name As String)

    Dim ws As Worksheet
    Set ws = ActiveWorkbook.Worksheets(p_ws_name)
    
    ws.Range("P2") = p_big_tickers(0)
    ws.Range("Q2") = p_big_percent_yearly_change(0)
    ws.Range("Q2").NumberFormat = "0.00%"
    ws.Range("P3") = p_big_tickers(1)
    ws.Range("Q3") = p_big_percent_yearly_change(1)
    ws.Range("Q3").NumberFormat = "0.00%"
    ws.Range("P4") = p_big_tickers(2)
    ws.Range("Q4") = p_big_ticker_volume
End Sub