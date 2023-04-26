library(shiny)
library(quantmod) 

# Define UI for app that draws a histogram ----
ui <- fluidPage(
  
  # App title ----
  titlePanel("Turtle Trading system 4T"),
  
  # Sidebar layout with input and output definitions ----
  sidebarLayout(
    
    # Sidebar panel for inputs ----
    sidebarPanel(
      dateInput('dateStart',
                label = 'Date Start : yyyy-mm-dd',
                value = as.Date("2020-01-01")
      ),
      dateInput('dateEnd',
                label = 'Date End: yyyy-mm-dd',
                value = as.Date("2023-01-01")
      ),
      numericInput("DC_O", "Donchian Open", value= 55),
      checkboxInput("DC_O_disp", "", value = TRUE),
      numericInput("DC_C", "Donchian Close", value= 20),
      checkboxInput("DC_C_disp", "", value = TRUE),
      numericInput("ATR", "ATR", value= 20),
      checkboxInput("ATR_disp", "", value = TRUE)
    ),
    
    # Main panel for displaying outputs ----
    mainPanel(
      
      # Output: Histogram ----
      plotOutput(outputId = "distPlot")
      
    )
  )
)

# Define server logic required to draw a histogram ----
server <- function(input, output) {
  
  # Histogram of the Old Faithful Geyser Data ----
  # with requested number of bins
  # This expression that generates a histogram is wrapped in a call
  # to renderPlot to indicate that:
  #
  # 1. It is "reactive" and therefore should be automatically
  #    re-executed when inputs (input$bins) change
  # 2. Its output type is a plot
  output$distPlot <- renderPlot({
    # getSymbols BTC-USD into df
    df <- getSymbols(Symbols = "BTC-USD", auto.assign = FALSE, from=input$dateStart, to=input$dateEnd, legend="")
    # Create chart Visualisation 
    chartSeries(df, up.col="green",dn.col="red")
    # Create Technical Analysis
    # Add TA to chart
    if (input$DC_O_disp) {
      dc20 <- DonchianChannel(HL(df), n=input$DC_O)[,c("high")]
      print(addTA(dc20, legend="Donchian 20", on=1, col=c("white")))
    }
    if (input$DC_C_disp) {
      dc10 <- DonchianChannel(HL(df), n=input$DC_C)[,c("low")]
      print(addTA(dc10, legend="Donchian 10", on=1, col=c("deepskyblue")))
    }
    if (input$ATR_disp) {
      atr <- ATR(HLC(df), n=input$ATR)$atr
      print(addTA(atr, legend="ATR", col="white"))
    }
  })
  
}

shinyApp(ui = ui, server = server)
