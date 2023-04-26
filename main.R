# Load packages
library(quantmod) 
library(TTR)
library(dplyr)
library(tibble)

# getSymbols BTC-USD into df
df <- getSymbols(Symbols = "BTC-USD", auto.assign = FALSE, from=as.Date("2023-01-01"))
df <- getSymbols(Symbols = "BTC-USD", auto.assign = FALSE, from=as.Date("2018-01-01"))

# Create chart Visualisation 
chartSeries(df, up.col="green",dn.col="red")
# Create Technical Analysis
dc20 <- DonchianChannel(HL(df), n=20)
dc10 <- DonchianChannel(HL(df), n=10)
atr <- ATR(HLC(df), n=14)$atr
# Add TA to chart
addTA(dc20, legend="Donchian 20", on=1, col=c("red", "yellow", "red"))
addTA(dc10, legend="Donchian 10", on=1, col=c("green", "yellow", "green"))
addTA(atr, legend="ATR", col="white")


trades <- function(df, O=20, C=10, A=14) {
  # Create TA
  dcO <- DonchianChannel(HL(df), n=O)
  dcC <- DonchianChannel(HL(df), n=C)
  atr <- ATR(HLC(df), n=A)$atr
  
  # Create signal data.frame
  signal <- data.frame(  
    (Hi(df) >= dcO$high),  
    (Lo(df) <= dcO$low),  
    (Lo(df) <= dcC$low),
    (Hi(df) >= dcC$high)
  )
  colnames(signal) <- c("buyO", "sellO", "buyC", "sellC")
  tail(signal)
  n <- nrow(signal)
  
  # Initialize result data.frame of positions
  result = data.frame(matrix(nrow = n, ncol = 6)) 
  colnames(result) <- c("bRISK", "bEARN", "bDATE", "sRISK", "sEARN", "sDATE")
  rownames(result) <- rownames(signal)
  
  # Get profit if price1 < price2 and is a buy it is profitable
  getProfit = function(i1, i2, buy=TRUE) {
    price1 <- as.double(Cl(df[i1]))
    price2 <- as.double(Cl(df[i2]))
    if (buy) {
      return (price2/price1)
    } else {
      return (price1/price2)
    }
  }
  
  # Get risk
  getRisk = function(i, buy=TRUE) {
    if (buy) {
      PRICE_val = Cl(df[i])
      SL_val = dcC$low[i]
      ATR_val = atr[i]
      return ((PRICE_val-SL_val)/ATR_val)
    } else {
      PRICE_val = Cl(df[i])
      SL_val = dcC$high[i]
      ATR_val = atr[i]
      return ((SL_val-PRICE_val)/ATR_val)
    }
  }
  
  # Filling result
  bDATE <- NA
  sDATE <- NA
  for (i in n:(O+1)) {
    if (!is.na(bDATE) && signal$buyO[i]) {
      result[i, "bDATE"] <- bDATE
      result[i, "bEARN"] <- getProfit(i, bDATE, buy=TRUE)
      result[i, "bRISK"] <- getRisk(i, buy=TRUE)
    } 
    if (!is.na(sDATE) && signal$sellO[i]) {
      result[i, "sDATE"] <- sDATE
      result[i, "sEARN"] <- getProfit(i, sDATE, buy=FALSE)
      result[i, "sRISK"] <- getRisk(i, buy=FALSE)
    } 
    if (signal$buyC[i]) {
      bDATE <- i
    }
    if (signal$sellC[i]) {
      sDATE <- i
    }
  }
  return (result)
}

afficher = function(df, result) {
  chartSeries(df, up.col="green",dn.col="red")
  result[c("sCUMULlog", "bCUMULlog")] <- result %>% 
    select(sCUMUL, bCUMUL) %>% 
    log10()
  xts_result <- result %>% 
    as.xts(index(df))
  addTA(xts_result$sCUMULlog)
  Sys.sleep(1)
  addTA(xts_result$bCUMULlog)
}
afficher(df, result)
chartSeries(df, up.col="green",dn.col="red")
result[c("sCUMULlog", "bCUMULlog")] <- result %>% 
  select(sCUMUL, bCUMUL) %>% 
  log10()
xts_result <- result %>% 
  as.xts(index(df))
addTA(xts_result$sCUMULlog)
addTA(xts_result$bCUMULlog)
Sys.sleep(1)



df <- getSymbols(Symbols = "BTC-USD", auto.assign = FALSE, from=as.Date("2020-01-01"))
result <- trades(df)

# Analyse EARN
result$bEARN <- result$bEARN %>% na.fill(fill=1)
result$sEARN <- result$sEARN %>% na.fill(fill=1)
prod(result$bEARN)
prod(result$sEARN)
# Cumulative gain
result <- result %>%
  mutate(
    bCUMUL = cumprod(bEARN), sCUMUL = cumprod(sEARN),
    bEARNpow = bEARN**(bRISK/3.9), sEARNpow = sEARN**sRISK,
    bCUMULpow = cumprod(bEARNpow), sCUMULpow = cumprod(sEARNpow))

# Create chart Visualisation
chartSeries(df, up.col="green",dn.col="red")
addTA(as.xts(result, index(df))$sCUMUL)
addTA(atr)

TA()

dc20 <- DonchianChannel(HL(df), n=20)
addTA(dc20$high)
dc20$one <- 1 
addTA(dc20$one)
addTA(sCUMUL)
# 
afficher(df, result)

result %>% 
  filter(!is.na(bRISK)) %>% 
  select(bRISK, bEARN, bEARNpow, bCUMUL, bCUMULpow) 

result %>% 
  filter(!is.na(bRISK)) %>% 
  filter(bEARN>1) %>% 
  summarise(mean(bRISK))

result %>% 
  filter(!is.na(bRISK)) %>% 
  filter(bEARN<1) %>% 
  summarise(mean(bRISK))
  
  
summarise(result)

head(result)







































