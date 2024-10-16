# brench ssa_brench.toml | python3 ../plot_benchmark.py output.png

import sys
import pandas as pd
import matplotlib.pyplot as plt

# Function to read from stdin with proper cleanup
def read_data_from_stdin():
    input_data = sys.stdin.read().strip().split('\n')
    header = input_data[0].strip().split(',')
    
    # Read the data into a list of dictionaries and remove extra spaces
    data = [dict(zip(header, [item.strip() for item in line.split(',')])) for line in input_data[1:]]
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Ensure 'result' is properly converted to numeric
    df['result'] = pd.to_numeric(df['result'], errors='raise')  # Raise error if conversion fails
    return df

# Function to plot the data and save it to a file
def plot_and_save(df, output_path):
    df_pivot = df.pivot(index='benchmark', columns='run', values='result')
    
    # Reorder the columns to make 'ssa_baseline' appear in the middle
    if 'ssa_baseline' in df_pivot.columns:
        df_pivot = df_pivot[['baseline', 'ssa_baseline', 'ssa']]
    
    # Dynamically calculate figure size based on the number of benchmarks and runs
    num_benchmarks = len(df_pivot.index)
    num_runs = len(df_pivot.columns)
    
    # Set width proportional to number of benchmarks and height to number of runs
    fig_width = max(8, num_benchmarks * 1.5)  # Minimum width of 8, scale by benchmarks
    fig_height = max(6, num_runs * 1.5)       # Minimum height of 6, scale by runs
    
    df_pivot.plot(kind='bar', figsize=(fig_width, fig_height))
    plt.title('Benchmark Results Comparison')
    plt.ylabel('Result')
    plt.xlabel('Benchmark')
    plt.xticks(rotation=45)
    plt.legend(title='Run')
    plt.tight_layout()
    plt.savefig(output_path)

# Main function
if __name__ == '__main__':
    # Read data from stdin
    df = read_data_from_stdin()
    
    # Define the output path (replace 'output.png' with the desired path)
    output_path = sys.argv[1]  # Pass the output path as a command line argument
    
    # Plot and save the figure
    plot_and_save(df, output_path)
    print(f"Plot saved to {output_path}")
