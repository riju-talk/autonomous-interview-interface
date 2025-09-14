"""Initialize database with sample Excel interview questions."""

import asyncio
import json
from app.core.database import get_db, init_db
from app.models.interview import Question, QuestionType, DifficultyLevel
from app.crud.interview import question as crud_question


async def create_sample_questions():
    """Create sample Excel interview questions."""
    
    sample_questions = [
        # Easy Excel Questions
        {
            "category": "Excel Basics",
            "difficulty": DifficultyLevel.EASY,
            "question_type": QuestionType.OBJECTIVE,
            "prompt": "What Excel function would you use to find the sum of values in a range?",
            "correct_answer": {"function": "SUM", "syntax": "=SUM(range)", "example": "=SUM(A1:A10)"},
            "explanation": "The SUM function adds all numbers in a range. Syntax: =SUM(range).",
        },
        {
            "category": "Excel Basics", 
            "difficulty": DifficultyLevel.EASY,
            "question_type": QuestionType.OBJECTIVE,
            "prompt": "How do you create a basic formula in Excel to multiply two cells?",
            "correct_answer": {"operation": "multiplication", "syntax": "=A1*B1", "example": "=A1*B1"},
            "explanation": "Use the asterisk (*) operator to multiply cells: =A1*B1",
        },
        
        # Medium Excel Questions
        {
            "category": "Excel Functions",
            "difficulty": DifficultyLevel.MEDIUM,
            "question_type": QuestionType.OBJECTIVE,
            "prompt": "Create a VLOOKUP formula to find a customer's email from a table where customer ID is in A2, the lookup table is in columns D:F, and email is in the 3rd column.",
            "correct_answer": {"function": "VLOOKUP", "formula": "=VLOOKUP(A2,D:F,3,FALSE)", "explanation": "Exact match lookup"},
            "explanation": "VLOOKUP syntax: =VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup]). FALSE ensures exact match.",
        },
        {
            "category": "Excel Functions",
            "difficulty": DifficultyLevel.MEDIUM,
            "question_type": QuestionType.MULTI_TURN,
            "prompt": "You have sales data with dates in column A and amounts in column B. How would you calculate the total sales for the current month using a formula?",
            "correct_answer": {"functions": ["SUMIFS", "MONTH", "YEAR"], "approach": "Use SUMIFS with date criteria"},
            "explanation": "Use SUMIFS with MONTH and YEAR functions to filter by current month: =SUMIFS(B:B,A:A,'>='&DATE(YEAR(TODAY()),MONTH(TODAY()),1),A:A,'<'&DATE(YEAR(TODAY()),MONTH(TODAY())+1,1))",
        },
        
        # Hard Excel Questions
        {
            "category": "Advanced Excel",
            "difficulty": DifficultyLevel.HARD,
            "question_type": QuestionType.ASSIGNMENT,
            "prompt": "Create a dynamic dashboard that shows monthly sales trends. Include: 1) A pivot table summarizing sales by month and product category, 2) A chart showing the trend, 3) Conditional formatting to highlight months with sales below average.",
            "correct_answer": {"components": ["PivotTable", "Chart", "Conditional Formatting", "Dynamic formulas"], "skills": ["Data analysis", "Visualization", "Advanced formatting"]},
            "explanation": "This requires combining multiple Excel features: PivotTables for data summarization, charts for visualization, and conditional formatting for highlighting patterns.",
        },
        {
            "category": "Excel Formulas",
            "difficulty": DifficultyLevel.HARD,
            "question_type": QuestionType.OBJECTIVE,
            "prompt": "Write an array formula (or modern dynamic array formula) that returns the top 3 highest values from a range A1:A100 along with their corresponding row numbers.",
            "correct_answer": {"functions": ["LARGE", "INDEX", "MATCH", "ROW"], "modern_approach": "SORT and TAKE functions", "array_formula": "INDEX/MATCH with LARGE"},
            "explanation": "Use LARGE function with INDEX/MATCH for traditional approach, or SORT/TAKE for modern Excel versions.",
        },
        
        # Behavioral Questions
        {
            "category": "Excel Experience",
            "difficulty": DifficultyLevel.MEDIUM,
            "question_type": QuestionType.MULTI_TURN,
            "prompt": "Describe a time when you had to work with a large Excel dataset (10,000+ rows). What challenges did you face and how did you overcome them?",
            "correct_answer": {"challenges": ["Performance", "Data quality", "Analysis complexity"], "solutions": ["Efficient formulas", "Data cleaning", "Pivot tables", "Power Query"]},
            "explanation": "Look for experience with large datasets, understanding of Excel limitations, and practical solutions.",
        },
        
        # Power Query and Advanced Features
        {
            "category": "Power Query",
            "difficulty": DifficultyLevel.HARD,
            "question_type": QuestionType.MULTI_TURN,
            "prompt": "You need to combine data from multiple CSV files in a folder. Each file has the same structure but different months of data. How would you automate this process in Excel?",
            "correct_answer": {"tool": "Power Query", "steps": ["From Folder", "Combine Files", "Transform data", "Load to worksheet"], "benefits": ["Automation", "Refresh capability", "Data consistency"]},
            "explanation": "Power Query's 'From Folder' feature can automatically combine multiple files with the same structure.",
        }
    ]
    
    async for db in get_db():
        for q_data in sample_questions:
            # Check if question already exists
            existing = await crud_question.get_by_category(db, category=q_data["category"])
            category_questions = [q for q in existing if q.prompt == q_data["prompt"]]
            
            if not category_questions:
                question = Question(**q_data)
                db.add(question)
        
        await db.commit()
        print(f"Created {len(sample_questions)} sample Excel interview questions!")


async def main():
    """Initialize database and create sample data."""
    print("Initializing database...")
    await init_db()
    
    print("Creating sample Excel interview questions...")
    await create_sample_questions()
    
    print("Database initialization complete!")


if __name__ == "__main__":
    asyncio.run(main())