# Autonomous Interview Interface - Frontend

A modern, interactive interview interface built with React, TypeScript, and Vite. This frontend application provides a seamless interview experience with real-time question management, timing, and evaluation features.

## Features

- **Interactive Interview Flow**: Step-by-step question navigation with progress tracking
- **Time Management**: Per-question timers with automatic submission on timeout
- **Session Persistence**: Resume interviews where you left off (stored in sessionStorage)
- **Responsive Design**: Works on desktop and tablet devices
- **Accessibility**: Built with accessibility in mind, following WAI-ARIA guidelines
- **Comprehensive Feedback**: Detailed evaluation and feedback after interview completion

## Tech Stack

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS with CSS Modules
- **State Management**: React Hooks & Context API
- **UI Components**: Custom component library built on Radix UI primitives
- **API Client**: Axios with interceptors for error handling
- **Testing**: Jest & React Testing Library

## Project Structure

```
src/
├── components/           # Reusable UI components
│   ├── ui/              # Radix-based UI primitives
│   ├── InterviewWindow/ # Main interview interface
│   └── Completion/      # Post-interview summary
├── hooks/               # Custom React hooks
├── lib/                 # Utility functions and API client
└── pages/               # Application pages
```

## Getting Started

### Prerequisites

- Node.js 16+ and npm 8+
- Backend API (FastAPI) should be running

### Installation

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd autonomous-interview-interface/apps/web
   ```

2. Install dependencies:
   ```sh
   npm install
   # or
   yarn
   ```

3. Create a `.env` file in the project root with the following variables:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```

4. Start the development server:
   ```sh
   npm run dev
   # or
   yarn dev
   ```

5. Open [http://localhost:5173](http://localhost:5173) in your browser.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run test` - Run tests
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

## API Integration

The frontend communicates with the following API endpoints:

- `POST /sessions/` - Create a new interview session
- `POST /sessions/{id}/messages` - Submit an answer
- `GET /sessions/{id}/evaluation` - Get evaluation results
- `GET /questions/pool` - Get available questions (optional)

## State Management

The application uses React's built-in state management with custom hooks:

- `useInterviewState` - Manages interview state (questions, answers, progress)
- `useQuestionTimer` - Handles per-question timing
- `useApi` - Handles API calls with loading/error states

## Testing

Run the test suite with:

```sh
npm test
```

Test coverage can be generated with:

```sh
npm test -- --coverage
```

## Deployment

Build the application for production:

```sh
npm run build
```

The build artifacts will be stored in the `dist/` directory.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Base URL for the API | `http://localhost:8000` |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Project Link: [https://github.com/yourusername/autonomous-interview-interface](https://github.com/yourusername/autonomous-interview-interface)
- Edit files directly within the Codespace and commit and push your changes once you're done.

## What technologies are used for this project?

This project is built with:

- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS

## How can I deploy this project?

Simply open [Lovable](https://lovable.dev/projects/f02badab-df7e-467f-a744-68922f59f4ba) and click on Share -> Publish.

## Can I connect a custom domain to my Lovable project?

Yes, you can!

To connect a domain, navigate to Project > Settings > Domains and click Connect Domain.

Read more here: [Setting up a custom domain](https://docs.lovable.dev/tips-tricks/custom-domain#step-by-step-guide)
