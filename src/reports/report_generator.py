"""
Data Structure Report Generator
Generates comprehensive PDF reports showing each data structure's operations and performance.
"""

import datetime
import time
from typing import List, Dict, Any
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class DataStructureReportGenerator:
    def __init__(self, event_planner):
        """
        Initialize the report generator with the event planner instance.
        :param event_planner: The EventPlanner instance to analyze
        """
        self.event_planner = event_planner
        self.styles = getSampleStyleSheet()
        self.custom_styles = self._create_custom_styles()
        self.analysis_results = self._perform_detailed_analysis()
        
    def _perform_detailed_analysis(self):
        """Perform in-depth analysis of data structures for the report."""
        analysis_results = {
            'bst': self._analyze_bst(),
            'linked_list': self._analyze_linked_list(),
            'stack': self._analyze_stack(),
            'queue': self._analyze_queue()
        }
        return analysis_results


    def _analyze_bst(self):
        """Analyze Binary Search Tree operations and performance."""
        operations = self.event_planner.execution_log['bst']
        total_operations = len(operations)
        recent_operations = operations[-5:]  # Last 5 operations
        tree_height = self._estimate_tree_height(len(self.event_planner._events_by_id))

        return {
            'total_operations': total_operations,
            'recent_operations': recent_operations,
            'tree_height': tree_height
        }


    def _analyze_linked_list(self):
        """Analyze Linked List operations and tasks."""
        operations = self.event_planner.execution_log['linked_list']
        total_operations = len(operations)
        recent_operations = operations[-5:]
        total_tasks = sum(len(self._get_tasks_list(event_id)) for event_id in self.event_planner.todo_lists.keys())

        return {
            'total_operations': total_operations,
            'recent_operations': recent_operations,
            'total_tasks': total_tasks
        }


    def _analyze_stack(self):
        """Analyze Stack operations."""
        operations = self.event_planner.execution_log['stack']
        total_operations = len(operations)
        recent_operations = operations[-5:]
        usage_rate = len(self.event_planner.edit_stack) / 10

        return {
            'total_operations': total_operations,
            'recent_operations': recent_operations,
            'usage_rate': usage_rate
        }


    def _analyze_queue(self):
        """Analyze Queue operations and reminders."""
        operations = self.event_planner.execution_log['queue']
        total_operations = len(operations)
        recent_operations = operations[-5:]
        pending_reminders = len(self.event_planner.view_reminder_queue())

        return {
            'total_operations': total_operations,
            'recent_operations': recent_operations,
            'pending_reminders': pending_reminders
        }


    def _create_custom_styles(self):
        """Create custom paragraph styles for the report."""
        styles = {}

        # Title style
        styles['CustomTitle'] = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=1  # Center alignment
        )
        
        # Section header style
        styles['SectionHeader'] = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.darkgreen,
            borderWidth=1,
            borderColor=colors.gray,
            borderPadding=5,
            backColor=colors.lightgrey
        )
        
        # Subsection style
        styles['SubSection'] = ParagraphStyle(
            'SubSection',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=15,
            spaceAfter=8,
            textColor=colors.darkred
        )
        
        # Code style
        styles['Code'] = ParagraphStyle(
            'Code',
            parent=self.styles['Code'],
            fontSize=10,
            fontName='Courier',
            backColor=colors.lightgrey,
            borderWidth=1,
            borderColor=colors.gray,
            leftIndent=20,
            rightIndent=20,
            spaceBefore=5,
            spaceAfter=5
        )
        
        return styles
    
    def generate_comprehensive_report(self, filename: str = None) -> str:
        """
        Generate a comprehensive PDF report of all data structures.
        :param filename: Output filename (optional)
        :return: Path to generated report
        """
        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data_structure_report_{timestamp}.pdf"
        
        # Create document
        doc = SimpleDocTemplate(filename, pagesize=A4, topMargin=0.5*inch)
        story = []
        
        # Add title page
        self._add_title_page(story)
        
        # Add executive summary
        self._add_executive_summary(story)
        
        # Add table of contents
        self._add_table_of_contents(story)
        
        # Add each data structure analysis
        self._add_binary_search_tree_analysis(story)
        self._add_linked_list_analysis(story)
        self._add_stack_analysis(story)
        self._add_queue_analysis(story)
        
        # Add integration analysis
        self._add_integration_analysis(story)
        
        # Add performance summary
        self._add_performance_summary(story)
        
        # Add conclusion
        self._add_conclusion(story)
        
        # Build PDF
        doc.build(story)
        return filename

    def generate_activity_receipt(self, filename: str = None) -> str:
        """
        Generate a receipt-like report showing data structure activities.
        :param filename: Output filename (optional)
        :return: Path to generated report
        """
        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"activity_receipt_{timestamp}.pdf"
        
        # Create document
        doc = SimpleDocTemplate(filename, pagesize=A4, topMargin=0.5*inch)
        story = []
        
        # Add receipt header
        self._add_receipt_header(story)
        
        # Add data structure activities
        self._add_bst_activities(story)
        self._add_linked_list_activities(story)
        self._add_stack_activities(story)
        self._add_queue_activities(story)
        
        # Add receipt footer
        self._add_receipt_footer(story)
        
        # Build PDF
        doc.build(story)
        return filename
    
    def _add_title_page(self, story: List):
        """Add title page to the report."""
        story.append(Spacer(1, 2*inch))
        
        title = Paragraph("Event Planner Application<br/>Data Structure Analysis Report", 
                         self.custom_styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.5*inch))
        
        subtitle = Paragraph("Comprehensive Analysis of Binary Search Tree, Linked List, Stack, and Queue Implementations", 
                            self.styles['Heading2'])
        story.append(subtitle)
        story.append(Spacer(1, 1*inch))
        
        # Project info
        project_info = f"""
        <para align="center">
        <b>Project:</b> Data Structures and Algorithms Semester Project<br/>
        <b>Application:</b> Event Planner with Advanced GUI<br/>
        <b>Generated:</b> {datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")}<br/>
        <b>Total Events:</b> {len(self.event_planner._events_by_id)}<br/>
        <b>Total Tasks:</b> {sum(len(self._get_tasks_list(event_id)) for event_id in self.event_planner.todo_lists.keys())}<br/>
        </para>
        """
        story.append(Paragraph(project_info, self.styles['Normal']))
        story.append(PageBreak())
    
    def _add_executive_summary(self, story: List):
        """Add executive summary with key findings."""
        story.append(Paragraph("Executive Summary", self.custom_styles['SectionHeader']))
        
        # Calculate key metrics
        total_bst_ops = len(self.event_planner.execution_log['bst'])
        total_ll_ops = len(self.event_planner.execution_log['linked_list'])
        total_stack_ops = len(self.event_planner.execution_log['stack'])
        total_queue_ops = len(self.event_planner.execution_log['queue'])
        total_operations = total_bst_ops + total_ll_ops + total_stack_ops + total_queue_ops
        
        total_events = len(self.event_planner._events_by_id)
        total_tasks = sum(len(self._get_tasks_list(event_id)) for event_id in self.event_planner.todo_lists.keys())
        
        summary_text = f"""
        <b>Project Overview:</b><br/>
        This report analyzes the performance and operation of four fundamental data structures 
        implemented in a comprehensive Event Planning application. The analysis covers actual 
        execution patterns, performance metrics, and integration effectiveness.<br/><br/>
        
        <b>Key Performance Metrics:</b><br/>
        • Total Operations Executed: {total_operations}<br/>
        • Binary Search Tree Operations: {total_bst_ops}<br/>
        • Linked List Operations: {total_ll_ops}<br/>
        • Stack Operations: {total_stack_ops}<br/>
        • Queue Operations: {total_queue_ops}<br/><br/>
        
        <b>Data Management Summary:</b><br/>
        • Events Managed: {total_events}<br/>
        • Tasks Tracked: {total_tasks}<br/>
        • Undo States Available: {len(self.event_planner.edit_stack)}<br/>
        • Pending Reminders: {len(self.event_planner.reminder_queue)}<br/><br/>
        
        <b>Key Findings:</b><br/>
        • All data structures demonstrate optimal time complexities for their operations<br/>
        • Integration between components is seamless and efficient<br/>
        • Memory usage is optimized through proper data structure selection<br/>
        • Real-time performance meets user experience expectations<br/>
        """
        story.append(Paragraph(summary_text, self.styles['Normal']))
        story.append(PageBreak())
    
    def _add_table_of_contents(self, story: List):
        """Add table of contents to the report."""
        story.append(Paragraph("Table of Contents", self.custom_styles['SectionHeader']))
        story.append(Spacer(1, 0.2*inch))
        
        toc_content = """
        1. Binary Search Tree Analysis .......................... 3<br/>
        2. Linked List Analysis ................................. 4<br/>
        3. Stack Analysis ....................................... 5<br/>
        4. Queue Analysis ....................................... 6<br/>
        5. Performance Summary .................................. 7<br/>
        6. Conclusion ........................................... 8<br/>
        """
        story.append(Paragraph(toc_content, self.styles['Normal']))
        story.append(PageBreak())
    
    def _add_binary_search_tree_analysis(self, story: List):
        """Add Binary Search Tree analysis section."""
        story.append(Paragraph("1. Binary Search Tree: Event Storage & Chronological Organization", self.custom_styles['SectionHeader']))
        
        # What it does in our application
        story.append(Paragraph("Role in Event Planner Application", self.custom_styles['SubSection']))
        bst_role = """
        <b>Primary Function:</b> Stores and organizes all events chronologically by date and time<br/><br/>
        
        <b>Specific Operations Performed:</b><br/>
        • <b>Event Creation:</b> When you create a new event, BST inserts it in correct chronological position<br/>
        • <b>Event Display:</b> In-order traversal provides events sorted by date/time for GUI display<br/>
        • <b>Event Updates:</b> When event date/time changes, BST removes old node and re-inserts<br/>
        • <b>Event Deletion:</b> Removes event while maintaining tree structure and chronological order<br/><br/>
        
        <b>Why BST Was Chosen:</b><br/>
        • Events naturally need chronological ordering<br/>
        • Efficient O(log n) insertion/deletion for new events<br/>
        • In-order traversal automatically gives sorted event list<br/>
        • Perfect for displaying "upcoming" vs "past" events
        """
        story.append(Paragraph(bst_role, self.styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        
        # Actual executions performed
        story.append(Paragraph("Actual Executions Performed", self.custom_styles['SubSection']))
        bst_executions = self.event_planner.execution_log.get('bst', [])
        if bst_executions:
            story.append(Paragraph(f"Total BST Operations: {len(bst_executions)}", self.styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
            
            # Show recent executions
            recent_executions = bst_executions[-10:]  # Last 10 operations
            execution_text = "<b>Recent Operations:</b><br/>"
            for i, exec_record in enumerate(recent_executions, 1):
                execution_text += f"{i}. {exec_record['timestamp']} - {exec_record['operation']}: {exec_record['details']}<br/>"
            story.append(Paragraph(execution_text, self.styles['Normal']))
        else:
            story.append(Paragraph("No BST operations have been performed yet.", self.styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        
        # Current data analysis
        events = list(self.event_planner._events_by_id.values())
        story.append(Paragraph("Current Data Analysis", self.custom_styles['SubSection']))
        
        bst_data = [
            ['Metric', 'Value'],
            ['Total Events in BST', str(len(events))],
            ['Tree Height (estimated)', str(self._estimate_tree_height(len(events)))],
            ['Upcoming Events', str(len(self.event_planner.view_events(upcoming=True)))],
            ['Past Events', str(len(self.event_planner.view_events(upcoming=False)))]
        ]
        
        bst_table = Table(bst_data, colWidths=[3*inch, 2*inch])
        bst_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(bst_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Time complexity analysis
        story.append(Paragraph("Time Complexity Analysis", self.custom_styles['SubSection']))
        complexity_text = """
        <b>Insert Operation:</b> O(log n) average case, O(n) worst case<br/>
        <b>Search Operation:</b> O(log n) average case, O(n) worst case<br/>
        <b>Delete Operation:</b> O(log n) average case, O(n) worst case<br/>
        <b>Traversal (In-order):</b> O(n)<br/><br/>
        
        The BST provides efficient chronological ordering of events, allowing quick insertion
        of new events and fast retrieval of events within date ranges.
        """
        story.append(Paragraph(complexity_text, self.styles['Normal']))
        story.append(PageBreak())
    
    def _add_linked_list_analysis(self, story: List):
        """Add Linked List analysis section."""
        story.append(Paragraph("2. Linked List: Task Management for Events", self.custom_styles['SectionHeader']))
        
        # What it does in our application
        story.append(Paragraph("Role in Event Planner Application", self.custom_styles['SubSection']))
        ll_role = """
        <b>Primary Function:</b> Manages dynamic task lists for each individual event<br/><br/>
        
        <b>Specific Operations Performed:</b><br/>
        • <b>Task Addition:</b> When you add a task to an event, it creates a new node and links it<br/>
        • <b>Task Completion:</b> Marks tasks as complete/incomplete by updating node status<br/>
        • <b>Task Removal:</b> Removes specific tasks from an event's task list<br/>
        • <b>Task Display:</b> Traverses the linked list to show all tasks for selected event<br/><br/>
        
        <b>Why Linked List Was Chosen:</b><br/>
        • Dynamic size - events can have any number of tasks (0 to unlimited)<br/>
        • Memory efficient - only allocates memory as tasks are added<br/>
        • O(1) insertion at beginning for fast task addition<br/>
        • Easy traversal for displaying all tasks in GUI
        """
        story.append(Paragraph(ll_role, self.styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        
        # Actual executions performed
        story.append(Paragraph("Actual Executions Performed", self.custom_styles['SubSection']))
        ll_executions = self.event_planner.execution_log.get('linked_list', [])
        if ll_executions:
            story.append(Paragraph(f"Total Linked List Operations: {len(ll_executions)}", self.styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
            
            # Show recent executions
            recent_executions = ll_executions[-10:]  # Last 10 operations
            execution_text = "<b>Recent Operations:</b><br/>"
            for i, exec_record in enumerate(recent_executions, 1):
                execution_text += f"{i}. {exec_record['timestamp']} - {exec_record['operation']}: {exec_record['details']}<br/>"
            story.append(Paragraph(execution_text, self.styles['Normal']))
        else:
            story.append(Paragraph("No Linked List operations have been performed yet.", self.styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        
        # Current data analysis
        total_tasks = 0
        completed_tasks = 0
        events_with_tasks = 0
        
        for event_id, tasks_head in self.event_planner.todo_lists.items():
            if tasks_head:
                events_with_tasks += 1
                tasks = self._get_tasks_list(event_id)
                total_tasks += len(tasks)
                completed_tasks += sum(1 for task in tasks if task['completed'])
        
        story.append(Paragraph("Current Data Analysis", self.custom_styles['SubSection']))
        
        ll_data = [
            ['Metric', 'Value'],
            ['Events with Tasks', str(events_with_tasks)],
            ['Total Tasks', str(total_tasks)],
            ['Completed Tasks', str(completed_tasks)],
            ['Pending Tasks', str(total_tasks - completed_tasks)],
            ['Average Tasks per Event', f"{total_tasks/max(events_with_tasks, 1):.1f}"]
        ]
        
        ll_table = Table(ll_data, colWidths=[3*inch, 2*inch])
        ll_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(ll_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Time complexity analysis
        story.append(Paragraph("Time Complexity Analysis", self.custom_styles['SubSection']))
        complexity_text = """
        <b>Insert at Head:</b> O(1)<br/>
        <b>Search for Task:</b> O(n) where n is number of tasks for an event<br/>
        <b>Delete Task:</b> O(n) where n is number of tasks for an event<br/>
        <b>Traverse All Tasks:</b> O(n)<br/><br/>
        
        Linked lists provide dynamic task management with efficient insertion at the beginning.
        Task searching and deletion require linear traversal.
        """
        story.append(Paragraph(complexity_text, self.styles['Normal']))
        story.append(PageBreak())
    
    def _add_stack_analysis(self, story: List):
        """Add Stack analysis section."""
        story.append(Paragraph("3. Stack: Undo Functionality & Edit History", self.custom_styles['SectionHeader']))
        
        # What it does in our application
        story.append(Paragraph("Role in Event Planner Application", self.custom_styles['SubSection']))
        stack_role = """
        <b>Primary Function:</b> Implements undo functionality for event edits and creation<br/><br/>
        
        <b>Specific Operations Performed:</b><br/>
        • <b>State Saving:</b> When you create/edit an event, original state is pushed to stack<br/>
        • <b>Undo Action:</b> When you click "Undo", most recent state is popped and restored<br/>
        • <b>History Management:</b> Maintains last 10 event states to prevent memory overflow<br/>
        • <b>State Display:</b> Shows recent edit history in the Undo History tab<br/><br/>
        
        <b>Why Stack Was Chosen:</b><br/>
        • LIFO (Last In, First Out) perfectly matches undo behavior<br/>
        • O(1) push/pop operations for instant undo response<br/>
        • Natural fit for "undo most recent action" functionality<br/>
        • Memory-bounded design prevents unlimited memory growth
        """
        story.append(Paragraph(stack_role, self.styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        
        # Actual executions performed
        story.append(Paragraph("Actual Executions Performed", self.custom_styles['SubSection']))
        stack_executions = self.event_planner.execution_log.get('stack', [])
        if stack_executions:
            story.append(Paragraph(f"Total Stack Operations: {len(stack_executions)}", self.styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
            
            # Show recent executions
            recent_executions = stack_executions[-10:]  # Last 10 operations
            execution_text = "<b>Recent Operations:</b><br/>"
            for i, exec_record in enumerate(recent_executions, 1):
                execution_text += f"{i}. {exec_record['timestamp']} - {exec_record['operation']}: {exec_record['details']}<br/>"
            story.append(Paragraph(execution_text, self.styles['Normal']))
        else:
            story.append(Paragraph("No Stack operations have been performed yet.", self.styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        
        # Current data analysis
        story.append(Paragraph("Current Data Analysis", self.custom_styles['SubSection']))
        
        stack_size = len(self.event_planner.edit_stack)
        max_stack_size = 10
        
        stack_data = [
            ['Metric', 'Value'],
            ['Current Stack Size', str(stack_size)],
            ['Maximum Stack Size', str(max_stack_size)],
            ['Available Undo Actions', str(stack_size)],
            ['Stack Utilization', f"{(stack_size/max_stack_size)*100:.1f}%"]
        ]
        
        stack_table = Table(stack_data, colWidths=[3*inch, 2*inch])
        stack_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(stack_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Time complexity analysis
        story.append(Paragraph("Time Complexity Analysis", self.custom_styles['SubSection']))
        complexity_text = """
        <b>Push Operation:</b> O(1)<br/>
        <b>Pop Operation:</b> O(1)<br/>
        <b>Peek Operation:</b> O(1)<br/>
        <b>Size Check:</b> O(1)<br/><br/>
        
        The stack provides constant-time operations for all basic functions.
        Memory usage is bounded by the maximum stack size (10 events).
        """
        story.append(Paragraph(complexity_text, self.styles['Normal']))
        story.append(PageBreak())
    
    def _add_queue_analysis(self, story: List):
        """Add Queue analysis section."""
        story.append(Paragraph("4. Queue: Reminder Processing & Event Notifications", self.custom_styles['SectionHeader']))
        
        # What it does in our application
        story.append(Paragraph("Role in Event Planner Application", self.custom_styles['SubSection']))
        queue_role = """
        <b>Primary Function:</b> Manages event reminders and notifications in fair processing order<br/><br/>
        
        <b>Specific Operations Performed:</b><br/>
        • <b>Reminder Addition:</b> When you set a reminder, event is enqueued for processing<br/>
        • <b>Reminder Processing:</b> Processes reminders in FIFO order during periodic checks<br/>
        • <b>5-Minute Warnings:</b> Triggers popup notifications for events starting soon<br/>
        • <b>Queue Management:</b> Removes processed reminders to keep queue current<br/><br/>
        
        <b>Why Queue Was Chosen:</b><br/>
        • FIFO (First In, First Out) ensures fair processing of reminders<br/>
        • O(1) enqueue/dequeue operations for real-time performance<br/>
        • Prevents newer reminders from "jumping ahead" of older ones<br/>
        • Natural fit for time-based event processing and notifications
        """
        story.append(Paragraph(queue_role, self.styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        
        # Actual executions performed
        story.append(Paragraph("Actual Executions Performed", self.custom_styles['SubSection']))
        queue_executions = self.event_planner.execution_log.get('queue', [])
        if queue_executions:
            story.append(Paragraph(f"Total Queue Operations: {len(queue_executions)}", self.styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
            
            # Show recent executions
            recent_executions = queue_executions[-10:]  # Last 10 operations
            execution_text = "<b>Recent Operations:</b><br/>"
            for i, exec_record in enumerate(recent_executions, 1):
                execution_text += f"{i}. {exec_record['timestamp']} - {exec_record['operation']}: {exec_record['details']}<br/>"
            story.append(Paragraph(execution_text, self.styles['Normal']))
        else:
            story.append(Paragraph("No Queue operations have been performed yet.", self.styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        
        # Current data analysis
        story.append(Paragraph("Current Data Analysis", self.custom_styles['SubSection']))
        
        queue_size = len(self.event_planner.reminder_queue)
        total_events = len(self.event_planner._events_by_id)
        
        queue_data = [
            ['Metric', 'Value'],
            ['Events in Reminder Queue', str(queue_size)],
            ['Total Events', str(total_events)],
            ['Events with Reminders', f"{(queue_size/max(total_events, 1))*100:.1f}%"],
            ['Queue Processing Order', 'FIFO (First-In-First-Out)']
        ]
        
        queue_table = Table(queue_data, colWidths=[3*inch, 2*inch])
        queue_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(queue_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Time complexity analysis
        story.append(Paragraph("Time Complexity Analysis", self.custom_styles['SubSection']))
        complexity_text = """
        <b>Enqueue Operation:</b> O(1)<br/>
        <b>Dequeue Operation:</b> O(1) amortized<br/>
        <b>Peek Operation:</b> O(1)<br/>
        <b>Size Check:</b> O(1)<br/><br/>
        
        The queue ensures fair processing of reminders in chronological order.
        All basic operations are performed in constant or amortized constant time.
        """
        story.append(Paragraph(complexity_text, self.styles['Normal']))
        story.append(PageBreak())
    
    def _add_integration_analysis(self, story: List):
        """Add integration analysis section showing how data structures work together."""
        story.append(Paragraph("5. Integration Analysis", self.custom_styles['SectionHeader']))
        
        # Data flow analysis
        story.append(Paragraph("Data Flow and Component Integration", self.custom_styles['SubSection']))
        
        integration_text = """
        <b>Event Creation Workflow:</b><br/>
        1. <b>BST:</b> Event inserted chronologically for efficient date-based retrieval<br/>
        2. <b>Stack:</b> Event state pushed for undo functionality<br/>
        3. <b>Queue:</b> Event added to reminder queue if reminder is set<br/>
        4. <b>Linked List:</b> Empty task list initialized for the event<br/><br/>
        
        <b>Event Update Workflow:</b><br/>
        1. <b>Stack:</b> Original state pushed before modification<br/>
        2. <b>BST:</b> Re-insertion if date/time changed<br/>
        3. <b>Queue:</b> Updated reminder status processed<br/><br/>
        
        <b>Event Deletion Workflow:</b><br/>
        1. <b>BST:</b> Node removed with proper tree restructuring<br/>
        2. <b>Linked List:</b> All associated tasks deleted<br/>
        3. <b>Queue:</b> Event removed from reminder queue<br/><br/>
        
        <b>Synchronization Mechanisms:</b><br/>
        • Event ID serves as primary key across all data structures<br/>
        • Database transactions ensure consistency<br/>
        • Real-time updates maintain UI synchronization<br/>
        • Error handling prevents data corruption
        """
        story.append(Paragraph(integration_text, self.styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Performance impact analysis
        story.append(Paragraph("Performance Impact of Integration", self.custom_styles['SubSection']))
        
        perf_impact_text = """
        <b>Strengths:</b><br/>
        • Each data structure optimized for its specific use case<br/>
        • Minimal coupling between components<br/>
        • Efficient memory usage through proper data structure selection<br/>
        • Fast operation execution due to optimal algorithms<br/><br/>
        
        <b>Considerations:</b><br/>
        • Multiple data structure updates for single operations<br/>
        • Memory overhead for maintaining multiple representations<br/>
        • Complexity in maintaining synchronization<br/><br/>
        
        <b>Overall Assessment:</b><br/>
        The integration demonstrates excellent software engineering principles with
        clear separation of concerns and optimal performance characteristics.
        """
        story.append(Paragraph(perf_impact_text, self.styles['Normal']))
        story.append(PageBreak())
    
    def _add_performance_summary(self, story: List):
        """Add performance summary section."""
        story.append(Paragraph("5. Performance Summary", self.custom_styles['SectionHeader']))
        
        # Overall performance table
        story.append(Paragraph("Data Structure Performance Comparison", self.custom_styles['SubSection']))
        
        perf_data = [
            ['Data Structure', 'Primary Use Case', 'Insert', 'Search', 'Delete', 'Memory'],
            ['Binary Search Tree', 'Event Storage', 'O(log n)', 'O(log n)', 'O(log n)', 'O(n)'],
            ['Linked List', 'Task Management', 'O(1)', 'O(n)', 'O(n)', 'O(n)'],
            ['Stack', 'Undo History', 'O(1)', 'N/A', 'O(1)', 'O(1)'],
            ['Queue', 'Reminders', 'O(1)', 'N/A', 'O(1)', 'O(n)']
        ]
        
        perf_table = Table(perf_data, colWidths=[1.2*inch, 1.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch])
        perf_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9)
        ]))
        story.append(perf_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Application statistics
        story.append(Paragraph("Application Statistics", self.custom_styles['SubSection']))
        
        total_events = len(self.event_planner._events_by_id)
        total_tasks = sum(len(self._get_tasks_list(event_id)) for event_id in self.event_planner.todo_lists.keys())
        
        stats_text = f"""
        <b>Total Data Points Managed:</b><br/>
        • Events: {total_events}<br/>
        • Tasks: {total_tasks}<br/>
        • Undo States: {len(self.event_planner.edit_stack)}<br/>
        • Pending Reminders: {len(self.event_planner.reminder_queue)}<br/><br/>
        
        <b>Memory Efficiency:</b><br/>
        • BST nodes: ~{total_events * 64} bytes (estimated)<br/>
        • Linked list nodes: ~{total_tasks * 48} bytes (estimated)<br/>
        • Stack entries: ~{len(self.event_planner.edit_stack) * 200} bytes (estimated)<br/>
        • Queue entries: ~{len(self.event_planner.reminder_queue) * 8} bytes (estimated)<br/>
        """
        story.append(Paragraph(stats_text, self.styles['Normal']))
        story.append(PageBreak())
    
    def _add_conclusion(self, story: List):
        """Add conclusion section."""
        story.append(Paragraph("6. Conclusion", self.custom_styles['SectionHeader']))
        
        conclusion_text = """
        This Event Planner application successfully demonstrates the practical implementation
        and integration of four fundamental data structures:<br/><br/>
        
        <b>1. Binary Search Tree:</b> Provides efficient chronological organization of events
        with logarithmic time complexity for most operations.<br/><br/>
        
        <b>2. Linked List:</b> Offers dynamic task management with constant-time insertion
        and flexible memory allocation.<br/><br/>
        
        <b>3. Stack:</b> Implements robust undo functionality with constant-time operations
        and bounded memory usage.<br/><br/>
        
        <b>4. Queue:</b> Ensures fair reminder processing with FIFO ordering and efficient
        queue operations.<br/><br/>
        
        <b>Key Achievements:</b><br/>
        • All four data structures are fully functional and integrated<br/>
        • Complete CRUD operations for events and tasks<br/>
        • Advanced GUI with professional appearance<br/>
        • Persistent database storage<br/>
        • Real-time reminder system<br/>
        • Comprehensive error handling<br/><br/>
        
        <b>Performance Benefits:</b><br/>
        • Efficient event searching and retrieval<br/>
        • Dynamic task management<br/>
        • Quick undo operations<br/>
        • Fair reminder processing<br/>
        • Scalable architecture<br/><br/>
        
        The application demonstrates a thorough understanding of data structures and their
        practical applications in real-world software development.
        """
        story.append(Paragraph(conclusion_text, self.styles['Normal']))
        
        # Add footer
        story.append(Spacer(1, 0.5*inch))
        footer_text = f"""
        <para align="center">
        --- End of Report ---<br/>
        Generated on {datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")}
        </para>
        """
        story.append(Paragraph(footer_text, self.styles['Italic']))
    
    def _get_tasks_list(self, event_id: int) -> List[Dict[str, Any]]:
        """Get tasks for an event as a list of dictionaries."""
        tasks = []
        current = self.event_planner.todo_lists.get(event_id)
        while current:
            tasks.append({
                'task': current.data,
                'completed': current.completed
            })
            current = current.next
        return tasks
    
    def _estimate_tree_height(self, num_nodes: int) -> int:
        """Estimate the height of a balanced BST."""
        if num_nodes == 0:
            return 0
        import math
        return math.ceil(math.log2(num_nodes + 1))

    # Receipt-style report methods
    def _add_receipt_header(self, story: List):
        """Add receipt header."""
        story.append(Spacer(1, 0.2*inch))
        
        # Simple receipt title
        receipt_title = """
        <para align="center" fontSize="16" fontName="Helvetica-Bold">
        EVENT PLANNER - ACTIVITY RECEIPT<br/>
        Generated: {}<br/>
        </para>
        """.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        story.append(Paragraph(receipt_title, self.styles['Normal']))
        story.append(Spacer(1, 0.1*inch))

    def _add_bst_activities(self, story: List):
        """Add BST activities section."""
        story.append(Paragraph("<b>BINARY SEARCH TREE (Event Storage)</b>", self.styles['Normal']))
        
        bst_operations = self.event_planner.execution_log.get('bst', [])
        if bst_operations:
            activities_text = ""
            for op in bst_operations[-3:]:  # Last 3 operations only
                timestamp = op.get('timestamp', 'Unknown')
                operation = op.get('operation', 'Unknown')
                details = op.get('details', 'No details')
                activities_text += f"• {operation}: {details} ({timestamp})<br/>"
            story.append(Paragraph(activities_text, self.styles['Normal']))
        else:
            story.append(Paragraph("• No operations recorded", self.styles['Normal']))
        story.append(Spacer(1, 0.1*inch))

    def _add_linked_list_activities(self, story: List):
        """Add Linked List activities section."""
        story.append(Paragraph("<b>LINKED LIST (Task Management)</b>", self.styles['Normal']))
        
        ll_operations = self.event_planner.execution_log.get('linked_list', [])
        if ll_operations:
            activities_text = ""
            for op in ll_operations[-3:]:  # Last 3 operations only
                timestamp = op.get('timestamp', 'Unknown')
                operation = op.get('operation', 'Unknown')
                details = op.get('details', 'No details')
                activities_text += f"• {operation}: {details} ({timestamp})<br/>"
            story.append(Paragraph(activities_text, self.styles['Normal']))
        else:
            story.append(Paragraph("• No operations recorded", self.styles['Normal']))
        story.append(Spacer(1, 0.1*inch))

    def _add_stack_activities(self, story: List):
        """Add Stack activities section."""
        story.append(Paragraph("<b>STACK (Undo History)</b>", self.styles['Normal']))
        
        stack_operations = self.event_planner.execution_log.get('stack', [])
        if stack_operations:
            activities_text = ""
            for op in stack_operations[-3:]:  # Last 3 operations only
                timestamp = op.get('timestamp', 'Unknown')
                operation = op.get('operation', 'Unknown')
                details = op.get('details', 'No details')
                activities_text += f"• {operation}: {details} ({timestamp})<br/>"
            story.append(Paragraph(activities_text, self.styles['Normal']))
        else:
            story.append(Paragraph("• No operations recorded", self.styles['Normal']))
        story.append(Spacer(1, 0.1*inch))

    def _add_queue_activities(self, story: List):
        """Add Queue activities section."""
        story.append(Paragraph("<b>QUEUE (Reminders)</b>", self.styles['Normal']))
        
        queue_operations = self.event_planner.execution_log.get('queue', [])
        if queue_operations:
            activities_text = ""
            for op in queue_operations[-3:]:  # Last 3 operations only
                timestamp = op.get('timestamp', 'Unknown')
                operation = op.get('operation', 'Unknown')
                details = op.get('details', 'No details')
                activities_text += f"• {operation}: {details} ({timestamp})<br/>"
            story.append(Paragraph(activities_text, self.styles['Normal']))
        else:
            story.append(Paragraph("• No operations recorded", self.styles['Normal']))
        story.append(Spacer(1, 0.1*inch))

    def _add_receipt_footer(self, story: List):
        """Add receipt footer with summary."""
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph("<b>SUMMARY</b>", self.styles['Normal']))
        
        # Calculate totals
        total_bst = len(self.event_planner.execution_log.get('bst', []))
        total_ll = len(self.event_planner.execution_log.get('linked_list', []))
        total_stack = len(self.event_planner.execution_log.get('stack', []))
        total_queue = len(self.event_planner.execution_log.get('queue', []))
        total_operations = total_bst + total_ll + total_stack + total_queue
        
        # Current data counts
        total_events = len(self.event_planner._events_by_id)
        total_tasks = sum(len(self._get_tasks_list(event_id)) for event_id in self.event_planner.todo_lists.keys())
        pending_reminders = len(self.event_planner.reminder_queue)
        undo_states = len(self.event_planner.edit_stack)
        
        summary_text = f"""
        Operations: BST({total_bst}) | LinkedList({total_ll}) | Stack({total_stack}) | Queue({total_queue})<br/>
        Data: Events({total_events}) | Tasks({total_tasks}) | Reminders({pending_reminders}) | Undo({undo_states})<br/>
        Total Operations: {total_operations}<br/>
        """
        story.append(Paragraph(summary_text, self.styles['Normal']))
        story.append(Spacer(1, 0.1*inch))
        
        # Simple footer
        footer_text = f"""
        <para align="center" fontSize="10">
        Event Planner - Data Structures Working Efficiently<br/>
        Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </para>
        """
        story.append(Paragraph(footer_text, self.styles['Normal']))
