def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()

def calculate_tdfi(df, lookback=13, filter_high=0.05, filter_low=-0.05):
    price = df['close']
    price_scaled = price * 1000

    mma = ema(price_scaled, lookback)
    smma = ema(mma, lookback)

    impetmma = mma.diff()
    impetsmma = smma.diff()
    divma = (mma - smma).abs()
    averimpet = (impetmma + impetsmma) / 2

    result = averimpet.copy()
    result = result * averimpet * averimpet  # power of 3

    tdf = divma * result
    ntdf = tdf / tdf.abs().rolling(window=lookback * 3).max()

    df['TDFI'] = ntdf
    df['Color'] = np.where(ntdf > filter_high, 'green',
                    np.where(ntdf < filter_low, 'red', 'gray'))
    return df

if __name__ == '__main__':
    df = fetch_ohlcv('ETH/USDT', '15m')
    if df is not None:
        df = calculate_tdfi(df)
        print(df[['timestamp', 'close', 'TDFI', 'Color']].tail())
