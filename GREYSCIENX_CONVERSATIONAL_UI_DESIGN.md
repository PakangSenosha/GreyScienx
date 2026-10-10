# GreyScienX Conversational UI Design

**Status:** Initial design specification  
**Surface:** GreyScienX website and AI-hosted interfaces  
**Purpose:** Define how GreyScienX should look and behave when an AI invokes its tools and presents results inside a conversation.

## 1. Design objective

GreyScienX should have one recognizable identity expressed through two purpose-built interfaces:

```text
GreyScienX backend and tool layer
├── GreyScienX website: complete product experience
└── AI-hosted UI: focused conversational widgets
```

The AI-hosted UI is not a miniature copy of the website. It is a compact, contextual expression of the same product. It should show only the information and actions needed for the user's current request, while the website remains the destination for deeper exploration and extended workflows.

## 2. Core principles

### One product, two surfaces

Both surfaces share the same brand foundations:

- Logo and product name
- Colour palette
- Typography and type scale
- Iconography
- Data-visualisation language
- Scientific terminology
- Confidence, risk and status conventions
- Tone of voice

Their layouts differ because their jobs differ:

- The website supports navigation, discovery and sustained work.
- The AI-hosted UI supports immediate understanding and focused action within a conversation.

### Conversation first

The component should answer the user's immediate question before exposing secondary detail. It should never reproduce a full dashboard when a concise result will do.

### Evidence over decoration

Scientific results should prioritise evidence, provenance, freshness and uncertainty. Visual elements must clarify the result rather than merely decorate it.

### Progressive disclosure

Show the conclusion first, then let the user inspect evidence, methodology and supporting data. Move complex analysis into an expanded or fullscreen view.

### Human control

Any action that changes data, starts a costly process or creates an external effect must be explicit and confirmable.

## 3. UI ownership and runtime model

When an AI calls a GreyScienX tool, the server may return structured data together with a registered UI resource. The host renders that component in a secure iframe alongside the conversation.

GreyScienX controls:

- The component's HTML, CSS and JavaScript
- Brand tokens and visual hierarchy
- Which result fields are displayed
- Interactive controls and local state
- Calls from the component back to GreyScienX tools
- Links into the full GreyScienX website

The AI host controls:

- The surrounding conversation
- Available presentation modes
- The container size and safe areas
- Theme, locale and host-level accessibility behaviour
- The model response before or after the component

New components should follow the open MCP Apps UI standard. ChatGPT-specific extensions should only be used when the shared standard does not provide the required capability.

## 4. Presentation modes

### Inline result card

Use for a single result, status, recommendation or confirmation.

Recommended content:

1. GreyScienX identity or result category
2. Clear result title
3. Primary finding
4. Confidence, risk or status
5. One compact evidence summary
6. One primary action and, if necessary, one secondary action

Example:

```text
GREYSCIENCX

Compound assessment
────────────────────────────────
Confidence                     92%
Primary finding                …
Risk level                Moderate

Based on 14 sources • Updated 2 min ago

[Explore evidence]   [Open in GreyScienX]
```

Rules:

- Do not add tabs or deep navigation.
- Avoid nested scrolling.
- Keep the result understandable at a glance.
- Use no more than two primary-area actions.
- Do not repeat information already stated clearly by the AI.

### Comparison list or carousel

Use when the user needs to compare a small number of similar candidates, compounds, sources or analyses.

Each item should expose the same fields in the same order:

- Name or identifier
- One differentiating visual
- Most relevant metric
- Confidence or status
- One short supporting line
- One focused action

Avoid presenting more items than a person can reasonably scan. Larger result sets should move to a list or fullscreen explorer.

### Fullscreen workspace

Use for work that genuinely requires space, including:

- Evidence exploration
- Scientific visualisations
- Multi-step analysis
- Editing structured inputs
- Comparing many candidates
- Reviewing provenance and methodology

The fullscreen view should still feel conversational. The user should be able to continue directing the AI while the workspace remains visible.

### Website handoff

Use **Open in GreyScienX** when the workflow requires:

- Long-running work
- Account administration
- Extensive navigation
- Saved projects or history
- Advanced configuration
- Large datasets
- Features that are not appropriate inside the conversational container

The handoff should preserve relevant context through a stable, authorized deep link where possible.

## 5. Visual system

### Shared design tokens

Create one source of truth for tokens used by both the website and conversational UI:

```text
colour.brand.primary
colour.brand.secondary
colour.semantic.success
colour.semantic.warning
colour.semantic.danger
colour.semantic.information
colour.surface.default
colour.surface.subtle
colour.text.primary
colour.text.secondary
colour.border.subtle

type.family.display
type.family.interface
type.size.title
type.size.body
type.size.caption

space.1 through space.8
radius.control
radius.panel
shadow.elevated
```

The AI-hosted UI may map these tokens to host theme values to support light and dark appearances without losing the GreyScienX identity.

### Brand presence

Branding should be unmistakable but restrained:

- Use the GreyScienX name or mark once near the result header.
- Use the brand accent for high-value actions and selected states.
- Avoid turning every border, icon or label into a branded element.
- Preserve neutral space around scientific information.

### Typography

- Use clear hierarchy before adding borders or containers.
- Use tabular numerals for measurements and comparisons.
- Keep supporting text concise.
- Do not shrink essential evidence or qualifications into unreadable captions.

### Scientific data

- Always include units.
- Keep decimal precision consistent within a comparison.
- Distinguish measured, predicted and inferred values.
- Never communicate risk by colour alone.
- Pair confidence indicators with plain-language meaning.
- Make timestamps and data freshness visible when relevant.

## 6. Component inventory

The initial conversational design system should contain:

### Foundations

- App header or identity strip
- Section heading
- Body and supporting text
- Divider
- Badge and status indicator
- Button and text action
- Tooltip or definition affordance
- Empty, loading and error states

### Scientific components

- Finding summary
- Confidence indicator
- Risk indicator
- Metric row
- Evidence source row
- Provenance summary
- Methodology disclosure
- Citation link
- Data-freshness indicator
- Compound or entity identity block
- Comparison row
- Compact chart or distribution view

### Workflow components

- Confirmation panel
- Editable parameter group
- Progress indicator
- Cancel or stop control
- Download or export action
- Open-in-GreyScienX action

## 7. Information hierarchy

Every result should answer these questions in order:

1. **What happened?** — The finding or outcome.
2. **How certain is it?** — Confidence, limitations and status.
3. **Why should I believe it?** — Evidence and provenance.
4. **What can I do next?** — One clear action.
5. **Where can I investigate further?** — Expanded view or website handoff.

Avoid leading with internal tool names, request identifiers or implementation details unless the user needs them for debugging.

## 8. Interaction model

### AI-to-component flow

1. The user expresses an intent in natural language.
2. The AI selects the appropriate GreyScienX data tool.
3. The data tool returns structured, model-readable results.
4. The AI may perform reasoning or choose relevant result identifiers.
5. A dedicated render tool returns the appropriate GreyScienX UI resource.
6. The component renders the result and exposes focused actions.

Data tools and render tools should remain separate. Search, computation and mutation tools should not automatically force the UI to re-render after every internal call.

### Component-to-tool flow

Interactive controls may call GreyScienX tools to:

- Refine an analysis
- Request additional evidence
- Change comparison criteria
- Confirm an operation
- Save a result
- Export data

Business data must remain on the server. Widget state is suitable for temporary presentation choices such as the selected item, expanded section or active filter; it is not a durable datastore.

## 9. Required states

Every component must define:

- Initial loading
- Partial or streaming result
- Complete result
- No result
- Recoverable error
- Permission or authentication required
- Stale data
- Long-running operation
- Cancelled operation
- Success confirmation

Error states should explain what the user can do next. Do not expose raw stack traces or internal server messages.

## 10. Responsive behaviour

Design for the narrow conversational container first.

- Use a single column by default.
- Let the host control the outer container.
- Avoid fixed widths and fixed heights.
- Do not use nested scrolling in inline views.
- Ensure controls remain reachable on small mobile screens.
- Move dense charts and multi-column comparisons to fullscreen.
- Respect host safe-area information and dynamic height changes.

## 11. Accessibility

Minimum requirements:

- Keyboard-operable controls
- Visible focus states
- Semantic headings and landmarks
- Accessible control names
- Sufficient text and control contrast
- Status communicated with text as well as colour
- Reduced-motion support
- Screen-reader descriptions for charts and scientific visuals
- Touch targets suitable for mobile use
- Logical reading and tab order

## 12. Trust, safety and scientific integrity

The conversational UI must make model and data limitations legible.

- Label generated, predicted and experimentally observed information.
- Show important uncertainty near the finding, not behind a distant disclosure.
- Preserve citations and provenance.
- Confirm consequential actions.
- Do not imply clinical, regulatory or scientific certainty beyond the evidence.
- Keep authorization and tenancy checks on the server.
- Never treat values supplied by the component as trusted without validation.
- Avoid putting sensitive business data into client-side state unless it is required for display.

## 13. Recommended implementation structure

```text
packages/
├── design-tokens/          Shared GreyScienX tokens
├── website-ui/             Full website components
└── conversational-ui/      AI-hosted components

apps/
├── web/                    GreyScienX website
└── mcp-ui/                 Bundled conversational widgets

services/
└── mcp-server/             Tools, UI resources and authorization
```

Recommended boundaries:

- Share tokens, icons and domain-specific visualisation logic.
- Do not share page layouts between the website and conversational UI.
- Keep tool schemas independent of React or another rendering framework.
- Version UI resources so deployed conversations do not unexpectedly change behaviour.
- Keep tools useful in clients that do not render UI.

## 14. Initial GreyScienX widget set

Build and validate these widgets first:

1. **Analysis summary** — finding, confidence, risk and next action.
2. **Evidence explorer** — sources, provenance and methodology.
3. **Candidate comparison** — consistent comparison across a small result set.
4. **Long-running job status** — progress, current phase and cancellation.
5. **Confirmation** — explicit review before a consequential operation.

This set establishes the core design language without recreating the full website inside the AI host.

## 15. Delivery phases

### Phase 1 — Brand extraction

- Inventory the existing website's colours, typography, icons and visual patterns.
- Convert them into shared tokens.
- Identify patterns that are unsuitable for a narrow conversational surface.

### Phase 2 — Core prototype

- Design the analysis-summary widget.
- Connect it to realistic GreyScienX tool output.
- Test light mode, dark mode, narrow mobile and desktop containers.

### Phase 3 — Interaction

- Add evidence expansion and focused refinement actions.
- Add fullscreen presentation for detailed exploration.
- Implement the website handoff with preserved context.

### Phase 4 — Validation

- Test keyboard and screen-reader behaviour.
- Test missing, partial, stale and failed data.
- Verify permission boundaries.
- Compare the widget with the website to confirm brand continuity.
- Run user testing on comprehension, confidence and next-action clarity.

## 16. Acceptance criteria

The first production widget is ready when:

- A user recognizes it as GreyScienX without mistaking it for the full website.
- The primary finding is understandable within a few seconds.
- Confidence, risk, evidence and freshness are represented accurately.
- The interface works in light and dark host themes.
- It remains usable at narrow mobile width.
- All controls work with keyboard and touch input.
- It uses no more than two primary-area actions.
- It has complete loading, empty, error and permission states.
- It can call the required GreyScienX tools securely.
- It offers an intentional handoff to the website for deeper work.
- The underlying tools remain usable without the widget.

## 17. Open design decisions

The following should be resolved before visual production begins:

- Canonical spelling and casing of the GreyScienX brand
- Final logo variants for light and dark surfaces
- Primary and semantic colour tokens
- Website typography that may legally and technically be embedded
- The first end-to-end user journey to support
- Which findings require explicit scientific disclaimers
- Which operations require confirmation
- Authentication and deep-link behaviour between ChatGPT and the website
- Data retention requirements for widget-visible information

## 18. Official references

- [Add UI to an MCP server](https://developers.openai.com/plugins/build/chatgpt-ui)
- [OpenAI plugin UI guidelines](https://developers.openai.com/plugins/concepts/ui-guidelines)
- [MCP server and UI quickstart](https://developers.openai.com/plugins/build/app-quickstart)
- [Plugin UI reference](https://developers.openai.com/plugins/reference)

