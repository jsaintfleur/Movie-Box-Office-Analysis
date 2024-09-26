import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual style for seaborn and matplotlib
sns.set(style="whitegrid")
plt.style.use('ggplot')

# Function to create 'images' directory if it doesn't exist
def create_images_directory():
    images_path = os.path.expanduser('~/Desktop/movies/images')
    if not os.path.exists(images_path):
        os.makedirs(images_path)
    return images_path

# Load and clean data
def load_and_clean_data(file_path):
    """
    Loads the CSV file, cleans the numeric columns, and formats the release date.
    """
    movies_box_office_df = pd.read_csv(file_path)
    movies_box_office_df['box office gross'] = movies_box_office_df['box office gross'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    movies_box_office_df['box office net'] = movies_box_office_df['box office net'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    movies_box_office_df['budget'] = movies_box_office_df['budget'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    movies_box_office_df['release date'] = pd.to_datetime(movies_box_office_df['release date'], errors='coerce')
    return movies_box_office_df

# Calculate profitability metrics
def calculate_profitability(df):
    df['profit'] = df['box office net'] - df['budget']
    df['profit margin (%)'] = (df['profit'] / df['budget']) * 100
    return df

# Visualization Functions
def visualize_genre_profitability(df, images_path):
    print("1. What is the most profitable movie genre overall?\n")
    genre_data = df.groupby('genre')['profit'].mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=genre_data.index.str.title(), y=genre_data.values, palette="Blues_d")
    plt.title("Average Profit by Genre", fontsize=16)
    plt.xlabel("Genre", fontsize=12)
    plt.ylabel("Average Profit (in billions)", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'genre_profitability.png'))
    plt.show()

def visualize_genre_profit_margin(df, images_path):
    print("2. What is the average profit margin for different genres?\n")
    genre_data = df.groupby('genre')['profit margin (%)'].mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=genre_data.index.str.title(), y=genre_data.values, palette="Oranges_d")
    plt.title("Average Profit Margin by Genre", fontsize=16)
    plt.xlabel("Genre", fontsize=12)
    plt.ylabel("Average Profit Margin (%)", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'genre_profit_margin.png'))
    plt.show()

def visualize_correlation_matrix(df, images_path):
    print("3. Is there a strong correlation between budget and box office gross?\n")
    plt.figure(figsize=(10, 8))
    correlation_matrix = df[['box office gross', 'box office net', 'budget', 'profit']].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title("Correlation Matrix of Box Office Metrics", fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'correlation_matrix.png'))
    plt.show()

def visualize_budget_vs_profit(df, images_path):
    print("4. Does a higher budget always result in a higher profit?\n")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='budget', y='profit', data=df, hue='genre', palette='Set1')
    plt.title("Budget vs Profit by Genre", fontsize=16)
    plt.xlabel("Budget (in billions)", fontsize=12)
    plt.ylabel("Profit (in billions)", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'budget_vs_profit.png'))
    plt.show()

def visualize_release_month_profit(df, images_path):
    print("5. Which month is the best to release a movie to maximize profit?\n")
    df['release month'] = df['release date'].dt.strftime('%B').str.title()
    month_data = df.groupby('release month')['profit'].mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=month_data.index, y=month_data.values, palette="Purples_d")
    plt.title("Average Profit by Release Month", fontsize=16)
    plt.xlabel("Release Month", fontsize=12)
    plt.ylabel("Average Profit (in billions)", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'release_month_profit.png'))
    plt.show()

def visualize_genre_vs_month(df, images_path):
    print("6. Are there specific times of the year when certain genres perform better?\n")
    df['release month'] = df['release date'].dt.strftime('%B').str.title()
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='release month', y='profit', hue='genre', data=df, palette="Set2")
    plt.title("Profit by Release Month and Genre", fontsize=16)
    plt.xlabel("Release Month", fontsize=12)
    plt.ylabel("Profit (in billions)", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'genre_vs_month.png'))
    plt.show()

def visualize_profit_margin_vs_budget(df, images_path):
    print("7. How does the profit margin vary between different budget sizes?\n")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='budget', y='profit margin (%)', data=df, hue='genre', palette='Dark2')
    plt.title("Budget vs Profit Margin", fontsize=16)
    plt.xlabel("Budget (in billions)", fontsize=12)
    plt.ylabel("Profit Margin (%)", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'profit_margin_vs_budget.png'))
    plt.show()

def visualize_box_office_net_vs_gross(df, images_path):
    print("8. What is the relationship between the box office net and box office gross?\n")
    plt.figure(figsize=(10, 6))
    sns.regplot(x='box office gross', y='box office net', data=df, scatter_kws={'s':50}, line_kws={'color':'red'})
    plt.title("Box Office Gross vs Net", fontsize=16)
    plt.xlabel("Box Office Gross (in billions)", fontsize=12)
    plt.ylabel("Box Office Net (in billions)", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'box_office_net_vs_gross.png'))
    plt.show()

def visualize_budget_break_even(df, images_path):
    print("9. Does the budget affect the likelihood of a movie breaking even or generating loss?\n")
    df['break even'] = df['profit'] > 0
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='break even', y='budget', data=df, palette="coolwarm")
    plt.title("Budget Size for Movies that Break Even vs Loss", fontsize=16)
    plt.xlabel("Break Even", fontsize=12)
    plt.ylabel("Budget (in billions)", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'budget_break_even.png'))
    plt.show()

def visualize_release_date_vs_profit_margin(df, images_path):
    print("10. How does the release date impact the overall profit margin for movies?\n")
    df['release month'] = df['release date'].dt.strftime('%B').str.title()
    month_data = df.groupby('release month')['profit margin (%)'].mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=month_data.index, y=month_data.values, palette="coolwarm")
    plt.title("Average Profit Margin by Release Month", fontsize=16)
    plt.xlabel("Release Month", fontsize=12)
    plt.ylabel("Profit Margin (%)", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(images_path, 'release_date_vs_profit_margin.png'))
    plt.show()

# Main function to run the analysis pipeline
def main(file_path):
    images_path = create_images_directory()
    movies_box_office_df = load_and_clean_data(file_path)
    movies_box_office_df = calculate_profitability(movies_box_office_df)

    # Answering business questions with visuals
    visualize_genre_profitability(movies_box_office_df, images_path)
    visualize_genre_profit_margin(movies_box_office_df, images_path)
    visualize_correlation_matrix(movies_box_office_df, images_path)
    visualize_budget_vs_profit(movies_box_office_df, images_path)
    visualize_release_month_profit(movies_box_office_df, images_path)
    visualize_genre_vs_month(movies_box_office_df, images_path)
    visualize_profit_margin_vs_budget(movies_box_office_df, images_path)
    visualize_box_office_net_vs_gross(movies_box_office_df, images_path)
    visualize_budget_break_even(movies_box_office_df, images_path)
    visualize_release_date_vs_profit_margin(movies_box_office_df, images_path)

# File path to the CSV file
file_path = os.path.expanduser('~/Desktop/movies/movies.csv')

# Run the analysis
if __name__ == '__main__':
    main(file_path)