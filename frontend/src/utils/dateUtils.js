import { format, parseISO, startOfWeek, endOfWeek } from 'date-fns'
import { ptBR } from 'date-fns/locale'

export const getLocalDate = (dateStr = null) => {
  if (dateStr) {
    const [year, month, day] = dateStr.split('-').map(Number)
    return new Date(year, month - 1, day)
  }
  return new Date()
}

export const formatDateForInput = (date) => {
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

export const formatDateForDisplay = (dateStr) => {
  if (!dateStr) return ''
  const date = getLocalDate(dateStr)
  return format(date, 'dd/MM/yyyy', { locale: ptBR })
}

export const validateTaskDate = (dateStr) => {
  return { isValid: true } 
}

export const validateDailySummaryDate = (dateStr) => {
  return { isValid: true } 
}

export const validateWeeklySummary = () => {
  return { isValid: true } 
}

export const getCurrentWeekPeriod = () => {
  const today = new Date()
  const weekStart = startOfWeek(today, { weekStartsOn: 1 }) 
  const weekEnd = endOfWeek(today, { weekStartsOn: 1 }) 
  
  return {
    start: formatDateForInput(weekStart),
    end: formatDateForInput(weekEnd),
    startFormatted: formatDateForDisplay(formatDateForInput(weekStart)),
    endFormatted: formatDateForDisplay(formatDateForInput(weekEnd))
  }
}