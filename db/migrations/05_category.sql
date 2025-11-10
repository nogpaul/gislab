-- 05_category.sql
ALTER TABLE public.places
  ADD COLUMN IF NOT EXISTS category text;

-- Example classifications (adjust as you like)
UPDATE public.places SET category = 'Residential Apparment'  WHERE name ILIKE '%Residential Apparment%';
UPDATE public.places SET category = 'Gas Station' WHERE name ILIKE '%Gas Station%';
UPDATE public.places SET category = 'Grocery Shop'   WHERE name ILIKE '%Grocery Shop%';

-- Optional: keep category non-null going forward
UPDATE public.places SET category = COALESCE(category, 'Other');

-- Optional: simple check list (relaxed for now; refine later)
-- ALTER TABLE public.places ADD CONSTRAINT chk_places_category
--   CHECK (category IN ('Residential Apparment','Gas Station','Grocery Shop','Other'));
