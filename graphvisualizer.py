import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime as dt
import os

print("\U0001F4E1 Downloading Bitcoin data...")
start_date = '2022-01-01'
end_date = dt.datetime.now().strftime('%Y-%m-%d')
data = yf.download('BTC-USD', start=start_date, end=end_date)

if data.empty:
    print("❌ Error: No data was downloaded. Check your internet or API limits.")
    exit()

# Reset index to ensure Date is a column
data.reset_index(inplace=True)

# If columns are a MultiIndex, flatten them to a single level.
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# Optionally, if the date column still isn't named correctly, you can rename it:
if 'Date' not in data.columns:
    # Assuming the first column is the date column
    data.rename(columns={data.columns[0]: 'Date'}, inplace=True)

# Ensure that the Date column is of datetime type
if not pd.api.types.is_datetime64_any_dtype(data['Date']):
    data['Date'] = pd.to_datetime(data['Date'])

print("✅ Data downloaded successfully!")
print("Columns after adjustment:", data.columns)
print(data.head())

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_title('Bitcoin Closing Price (2022 to Now)', fontsize=16)
ax.set_xlabel('Date', fontsize=14)
ax.set_ylabel('Closing Price (USD)', fontsize=14)
ax.grid(True)

ax.set_xlim(data['Date'].min(), data['Date'].max())
ax.set_ylim(data['Close'].min() * 0.95, data['Close'].max() * 1.05)

line, = ax.plot([], [], lw=2, color='blue')

# Define animation functions
def init():
    line.set_data([], [])
    return line,

def animate(i):
    x = data['Date'][:i]
    y = data['Close'][:i]
    line.set_data(x, y)
    return line,

print("\U0001F3A5 Creating animation...")
frame_skip = max(1, len(data) // 500)  # Limit frames for efficiency
ani = FuncAnimation(fig, animate, frames=range(0, len(data), frame_skip), init_func=init, interval=50, blit=False)

# Save animation
save_path = os.path.join(os.getcwd(), 'bitcoin_animation.mp4')
print(f"📝 Saving animation to: {save_path}")

def progress_callback(i, n):
    print(f"Saving frame {i}/{n}...")

try:
    ani.save(save_path, writer='ffmpeg', fps=30, progress_callback=progress_callback)
    print("✅ Animation saved successfully!")
except Exception as e:
    print(f"❌ Error saving animation: {e}")

print("\U0001F4FA Displaying animation...")
plt.show()
